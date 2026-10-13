# Cobbleverse Auto Tooltips (experimental)

Minecraft 1.21.1 • Fabric • Java 21 • **client only**.

## What it does

When a mod checks `Screen.hasShiftDown()` or `Screen.hasControlDown()`
during synchronous tooltip construction, this mod makes the answer `true`.
Regular gameplay and inventory keyboard shortcuts are unaffected because
the override is guarded by the current tooltip call stack.

The Sophisticated Backpacks (Unofficial Fabric port) 1.21.1 implementation
calls `Screen.hasShiftDown()` inside
`BackpackItemClient#getTooltipImage`, so its preview is covered.

## Limitations

- Not a universal solution: mods may read GLFW/keyboard state directly,
  cache key state, or request missing data from the server.
- Mods with custom tooltip renderers may need specific integration.
- The implementation does **not** make server-only item data appear on the client.
- This is an initial compatibility build; successful compilation alone does
  **not** prove no in-game crash with a particular modpack.

No Fabric API dependency; compatible with Fabric Loader 0.18.4.

## Build

With JDK 21 and Gradle 8.10.2:

`gradle --no-daemon clean build`

Install only the remapped `cobbleverse-auto-tooltips-0.1.0.jar`,
**not** a `-dev.jar`.
