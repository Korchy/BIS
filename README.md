# BIS
Blender Interplanety Storage (BIS) – the online material (shader) storage add-on for Blender 3D creation.

Author: Nikita Akimov interplanety@interplanety.org

BIS webpage: https://b3d.interplanety.org/en/bis-online-blender-material-storage/

BIS website: https://bis.interplanety.org/en

<img src = "https://b3d.interplanety.org/wp-content/upload_content/2018/05/01_670x335.jpg">

Current version:
-
1.3.3

Supported Blender versions:
-

2.78, 2.79

Installation and usage:
-
- Download zip archive with add-on distributive.
- In Blender: User Preferences — Add-ons — Install From File — specify downloaded archive.
- Through your favorite browser visit the BIS website and register your account.
- In Blender: Node Editor window – T-panel – BIS tab:
- Sign in with the username and password created on the BIS website.
- To save the group of nodes into the BIS storage, select the desired node group and click “Add nodegroup to BIS”. Specify description tags in the "Tag" field before saving.
- To restore nodegroup from the BIS storage – specify the name/tag in the “Search” field and click “Search in BIS”. Click on the preview window and select the necessary material from the drop-down list.
---
- 15 active cells are available. More materials stores to reserve pool. Send materials to reserve and restored currently needed to fit within available cells count.
- If the stored to BIS nodegroup uses textures, only the relative paths to textures are saved in BIS. Uploading such material from the BIS, the add-on searches for the used textures along the saved paths on the user’s local computer.
- Update materials previews images through the BIS website.

Version history:
-
1.3.3
- Automatically add Blender version to tags while storing material to BIS

1.3.2
- Automatically add render engine name and "procedural" (if node group is procedural) to tags while storing material to BIS

1.3.1
- Some bugs fixed

1.3.0
- Added the Open storage

1.2.0
- Node group storage divided to separate types: Shader, Compositing, World

1.1.1
- Added labels to preview images
- Fixed some bugs with "Frame" and "Reroute" nodes

1.1.0
- Preview automatically generation for procedural node groups added

1.0.1
- Internal code updates

1.0.0
- Release!
- The server part of the storage has been put in order.
- The external and internal design of the BIS website is finished.
- Fixed and corrected some add-on code.
- Updated the BIS description page.
- Fixed a number of minor bugs and errors.

0.0.3
- Supports all cyceles nodes
- Supports saving texts from Text editor

0.0.2
- Supports all cyceles nodes from groups (Shift + a): Input, Output, Shader, Texture, Color

0.0.1
- Early access
