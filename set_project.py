# URL: https://github.com/isLundy/Set-Project
# version: 1.0

def set_project():

    # check node numbers
    if len(nuke.selectedNodes()) == 1:
        # get node info
        node = nuke.selectedNode()
        first_frame = 1001
        last_frame = int(node['origlast'].getValue() - node['origfirst'].getValue() + first_frame)
        plate_width = int(node['format'].value().width())
        plate_height = int(node['format'].value().height())
        plate_pixelAspect = int(node['format'].value().pixelAspect())

        # set frame range
        nuke.root()['first_frame'].setValue(first_frame)
        nuke.root()['last_frame'].setValue(last_frame)

        # Move the current frame to the frame range
        if int(nuke.frame()) not in range(first_frame, last_frame+1):
            nuke.frame(first_frame)

        # set format
        existing_format = False
        formatNames = [format.name() for format in nuke.formats()]

        for format in nuke.formats():
            if (plate_width == int(format.width()) and
                plate_height == int(format.height()) and
                plate_pixelAspect == int(format.pixelAspect()) and
                format.name() and
                formatNames.count(format.name()) == 1):

                existing_format = True
                nuke.root()['format'].setValue(format.name())
                break

        if existing_format == False:
            if 'Plate' in formatNames:
                n = 2
                while f'Plate_{n}' in formatNames:
                    n += 1
                plate_name = f'Plate_{n}'

            else:
                plate_name = 'Plate'

            nuke.addFormat(f"{plate_width} {plate_height} {plate_pixelAspect} {plate_name}")
            nuke.root()['format'].setValue(plate_name)

        # set fps
        try:
            nuke.root()['fps'].setValue(round(node.metadata()['input/frame_rate'], 3))
        except:
            metadata_fps = [value for key, value in node.metadata().items() if 'frame_rate' in key]
            if metadata_fps:
                nuke.root()['fps'].setValue(round(metadata_fps[0], 3))
                print(metadata_fps)
            else:
                nuke.message('''Please set <span style="color: #FF9F0A">fps</span> manually in the <span style="color: rgb(255,159,10)">Project Settings</span>.'''
                            '''\n\nreason:'''
                            '''\nThe frame rate data doesn't exist.'''
                            )
                nuke.showSettings()
    # only one
    else:
        nuke.message('Please select a ReadNode node (only <span style="color: rgb(255,69,58)">one</span>).')

set_project()
