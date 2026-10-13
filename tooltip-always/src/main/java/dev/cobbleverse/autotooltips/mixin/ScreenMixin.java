package dev.cobbleverse.autotooltips.mixin;

import dev.cobbleverse.autotooltips.TooltipCallDetector;
import net.minecraft.client.gui.screen.Screen;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(Screen.class)
public abstract class ScreenMixin {
    @Inject(method = "hasShiftDown", at = @At("HEAD"), cancellable = true)
    private static void cobbleverse$expandShiftTooltip(CallbackInfoReturnable<Boolean> cir) {
        if (TooltipCallDetector.isTooltipCall()) {
            cir.setReturnValue(true);
        }
    }

    @Inject(method = "hasControlDown", at = @At("HEAD"), cancellable = true)
    private static void cobbleverse$expandControlTooltip(CallbackInfoReturnable<Boolean> cir) {
        if (TooltipCallDetector.isTooltipCall()) {
            cir.setReturnValue(true);
        }
    }
}
