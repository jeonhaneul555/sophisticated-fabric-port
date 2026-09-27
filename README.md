# Sophisticated Fabric 1.21.8 Port

Private porting workspace for Minecraft Java 1.21.8 + Fabric.

Target:
- Minecraft 1.21.8
- Fabric Loader 0.19.4
- Fabric API 0.136.1+1.21.8
- Java 21

Upstream Fabric bases:
- Salandora/SophisticatedCore (`1.21.x-fabric`)
- Salandora/SophisticatedBackpacks (`1.21.x-fabric`)

The GitHub Actions workflow clones the GPL Fabric bases, applies the 1.21.8 migration patch, builds Core first, then Backpacks, and uploads build logs/artifacts.
