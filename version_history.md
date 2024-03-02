Version history:
-
1.11.1
- Updated for compatibility with Blender 4.0

1.11.0
- Added support for Geometry Nodes

1.10.0
- Remove old versions compatibility
- Mesh storage modified to store from 'import' principles

1.9.2
- Fixed issue with textures path-names

1.9.1
- Fixed converting of all the materials in the BIS to new format. This version is fully compatible with old format in reading but writes materials only with the new format.

1.9.0
- Storage system changed to be more flexible to future changes (compatible with NodeTree Source)
- Updated for Blender 2.90, 2.91

1.8.4
- Updated some 2.83 nodes parameters

1.8.3
- Updated some nodes parameters
- Added saving blend mode property from material settings

1.8.2
- Updated some nodes parameters

1.8.1
- Add "Material: Active to Selected" button to "Tools" im meshes panel

1.8.0
- Add additional panel mode in 3D_VIEW window to assign materials to meshes directly in 3D viewport
- Some bug fixes

1.7.1
- Deselects all other nodes when adding node group from BIS
- Some inner engine changes

1.7.0
- Enabled storing materials with textures

1.6.5
- Added "Help" button with simple tips.

1.6.4
- Added option to work separalety with materials or node groups
- Uploaded node group adds to the current open node group instead of the node tree root
- Experimental mode can be enabled/disabled in add-on preferences

1.6.3
- Updated according the last Blender API version (2019.03.06)

1.6.2
- Some interface changes

1.6.1
- Fixing bugs

1.6.0
- Porting to Blender 2.80

1.5.2
- Added "Tools" section to Node editor panel
- Added "Add input/output" tool in Node editor "Tools"

1.5.1
- Added automatical preview generation for saved meshes
- Hided "search" field for free accounts

1.5.0
- Added storage for meshes

1.4.4
- Fixed some bugs with reroute node and inputs/outputs default values

1.4.3
- Fixed bug with several node groups enumeration

1.4.2
- Some internal technical changes in saving nogdes format (connecting links by inputs/outputs identifier)
- Added saved node groups version control

1.4.1
- Added "prev" and "next" page button for "pro" accounts
- Some changes on the server-side

1.4.0
- Added "update" functionality for nodegroups and texts

1.3.6
- Fixed some issues with saving script nodes

1.3.5
- Fixed some issues with nodes from future Blender versions

1.3.4
- Checked all compositing nodes, provided proper work with compositing node trees

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
