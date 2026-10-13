package dev.cobbleverse.autotooltips;

/** No Minecraft libraries needed. Run in CI with javac + java. */
public final class TooltipCallDetectorPolicyTest {
    private record Call(String owner, String method) {}
    private static Call f(String owner, String method) { return new Call(owner, method); }

    private static void expect(boolean wanted, String name, Call... calls) {
        var ctx = new TooltipCallDetector.Context();
        for (Call f : calls) ctx.accept(f.owner, f.method);
        if (ctx.shouldExpand() != wanted) throw new AssertionError(name);
    }

    public static void main(String[] args) {
        Call render = f("net.minecraft.class_465", "method_25394");
        Call tooltip = f("net.p3pp3rf1y.sophisticatedbackpacks.backpack.BackpackItemClient", "getTooltipImage");
        expect(true, "Backpack tooltips still expand", render, tooltip);
        expect(true, "Generic modded item tooltips expand",
            render, f("com.othermod.Item", "appendHoverText"));
        expect(false, "Render without tooltip", render);
        expect(false, "Tooltip assembled outside rendering", tooltip);
        expect(false, "Mouse input must not trigger virtual Shift",
            render, tooltip, f("net.minecraft.class_312", "method_1601"));
        expect(false, "Keyboard input must not trigger virtual Ctrl",
            render, tooltip, f("net.minecraft.class_309", "method_1454"));
        expect(false, "Container mouseClicked",
            render, tooltip, f("net.minecraft.class_465", "method_25402"));
        expect(false, "Container mouseDragged",
            render, tooltip, f("net.minecraft.class_465", "method_25403"));
        expect(false, "Container mouseReleased",
            render, tooltip, f("net.minecraft.class_465", "method_25406"));
        expect(false, "Slot quick move",
            render, tooltip, f("net.minecraft.class_465", "method_2383"));
        expect(false, "Modded input handler",
            render, tooltip, f("com.othermod.CustomScreen", "onMouseClicked"));
        System.out.println("11 tooltip/input regression checks passed");
    }
}
