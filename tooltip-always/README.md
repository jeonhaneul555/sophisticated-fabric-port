# Cobbleverse Auto Tooltips 0.2.0 (experimental)

Minecraft 1.21.1 • Fabric • Java 21 • **client only**

## Purpose

Reveal existing Shift/Ctrl-gated item tooltips and Sophisticated Backpacks
(Unofficial Fabric port) contents preview without holding a modifier key.

## Critical change from 0.1.0

Version 0.1.0 caused normal inventory clicks to behave as Shift+clicks.
**Remove 0.1.0 before installing 0.2.0.**

0.2.0 allows virtual modifiers only when *both* a tooltip and a rendering
method are on the current call stack. Mouse, keyboard, container-click,
drag, and quick-move handlers explicitly disable virtual modifiers.
When context is uncertain, actual keyboard state takes priority.

11 standalone regression cases assert the intended tooltip/input policy.
The Fabric build and JAR metadata are checked by GitHub Actions.

## Compatibility

- Minecraft 1.21.1 and Fabric Loader 0.18.4 / Java 21 are targeted.
- No Fabric API dependency; client-only mod.
- Mods that use direct GLFW key reads or custom tooltip systems may need adapters.
- Client-side tooltips cannot reveal server-only data.
- Successful compilation does not prove behavior in every modpack GUI.

## Build

JDK 21 and Gradle 8.10.2:

`gradle --no-daemon clean build`

Install `cobbleverse-auto-tooltips-0.2.0.jar` (not dev or sources JAR).
