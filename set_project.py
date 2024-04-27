def set_project():
    if len(nuke.selectedNodes()) == 1:
        node = nuke.selectedNode()
        first_frame = 1001
        last_frame = int(node['origlast'].getValue() - node['origfirst'].getValue() + first_frame)
        new_width = node['format'].value().width()
        new_height = node['format'].value().height()

        nuke.root()['first_frame'].setValue(first_frame)
        nuke.root()['last_frame'].setValue(last_frame)
        if nuke.frame() not in range(first_frame, last_frame+1):
            nuke.frame(first_frame)

        try:
            nuke.root()['fps'].setValue(round(node.metadata()['input/frame_rate'], 3))
        except: 
            nuke.message('''Please set <span style="color: #FF9F0A">fps</span> manually in the <span style="color: #FF9F0A">Project Settings</span>.'''
                        '''\n\nreason:'''
                        '''\nThe frame rate data doesn't exist for this plate.'''
                        )

        exist = False
        for format in nuke.formats():
            if int(new_width) == int(format.width()) and int(new_height) == int(format.height()):
                if format.name():
                    exist = True
                    nuke.root()['format'].setValue(format.name())
                    break

        if exist == False:
            nuke.addFormat(f"{new_width} {new_height} Plate")
            nuke.root()['format'].setValue('Plate')

    else:
        nuke.message('Please select a ReadNode node (only <span style="color:#FF453A">one</span>).')

set_project()