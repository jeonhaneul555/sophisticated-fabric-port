package dev.cobbleverse.autotooltips;

import java.lang.StackWalker;
import java.util.Locale;

/**
 * Limit virtual modifier keys to synchronous tooltip construction.
 *
 * Not a physical-key spoof: normal clicks, player controls and UI shortcuts
 * keep their real modifier state. Mods which read GLFW keys directly will
 * need an individual compatibility adapter.
 */
public final class TooltipCallDetector {
    private static final StackWalker WALKER = StackWalker.getInstance();

    private TooltipCallDetector() {}

    public static boolean isTooltipCall() {
        return WALKER.walk(frames -> frames
            .limit(48)
            .anyMatch(frame -> {
                String owner = frame.getClassName();
                if (owner.startsWith("dev.cobbleverse.autotooltips.")) {
                    return false;
                }

                String method = frame.getMethodName().toLowerCase(Locale.ROOT);
                return method.contains("tooltip")
                    || method.contains("hovertext")
                    || method.equals("appendhovertext")
                    || method.equals("addinformation");
            }));
    }
}
