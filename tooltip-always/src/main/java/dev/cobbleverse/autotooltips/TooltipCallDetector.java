package dev.cobbleverse.autotooltips;

import java.lang.StackWalker;
import java.util.Locale;

/**
 * Detects tooltip RENDER calls only. Never virtualizes modifiers while input
 * callbacks (mouse, keyboard, inventory clicks/drags) are executing.
 * Intermediary names below are verified for Minecraft 1.21.1.
 */
public final class TooltipCallDetector {
    private static final StackWalker WALKER = StackWalker.getInstance();

    private TooltipCallDetector() {}

    public static boolean isTooltipCall() {
        return WALKER.walk(frames -> {
            Context ctx = new Context();
            frames.limit(64).forEach(f -> ctx.accept(f.getClassName(), f.getMethodName()));
            return ctx.shouldExpand();
        });
    }

    static final class Context {
        private boolean tooltip;
        private boolean rendering;
        private boolean interacting;

        void accept(String owner, String method) {
            if (owner.startsWith("dev.cobbleverse.autotooltips.")) {
                return;
            }

            String lower = method.toLowerCase(Locale.ROOT);

            // When real mouse/keyboard callbacks are active, always keep the
            // genuine keyboard state. Covers both dev and production mappings.
            if (owner.equals("net.minecraft.class_312")
                || owner.equals("net.minecraft.client.Mouse")
                || owner.equals("net.minecraft.class_309")
                || owner.equals("net.minecraft.client.Keyboard")) {
                interacting = true;
            }

            // Vanilla HandledScreen inventory click/drag/quick-move paths.
            if (owner.equals("net.minecraft.class_465")
                || owner.equals("net.minecraft.client.gui.screen.ingame.HandledScreen")) {
                if (method.equals("method_25402") || method.equals("mouseClicked")
                    || method.equals("method_25403") || method.equals("mouseDragged")
                    || method.equals("method_25406") || method.equals("mouseReleased")
                    || method.equals("method_2383") || method.equals("onMouseClick")
                    || method.equals("method_30107")) {
                    interacting = true;
                }
            }

            // Also catch named hooks from third-party GUIs.
            if (lower.contains("mouseclicked")
                || lower.contains("mousedragged")
                || lower.contains("mousereleased")
                || lower.contains("onmouseclick")
                || lower.contains("slotclick")
                || lower.contains("quickmove")
                || lower.contains("shiftclick")
                || lower.contains("keypressed")
                || lower.contains("keyreleased")) {
                interacting = true;
            }

            if (lower.contains("tooltip")
                || lower.contains("hovertext")
                || lower.equals("addinformation")) {
                tooltip = true;
            }

            // Guard: tooltips assembled during slot actions must not virtualize
            // Shift/Ctrl. Only expand during a render frame.
            if (method.equals("method_25394")
                || method.equals("render")
                || lower.equals("drawscreen")) {
                rendering = true;
            }
        }

        boolean shouldExpand() {
            return tooltip && rendering && !interacting;
        }
    }
}
