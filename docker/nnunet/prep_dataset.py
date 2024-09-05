for x in range(40):

    if x > 20:
        target_img = 'imagesTr'
        target_lb = 'labelsTr'
    else:
        target_img = 'imagesTs'
        target_lb = 'labelsTs'

        case_folder = f's{x:04d}'
        command = f'cp {case_folder}/ct.nii.gz {target_img}/{x:04d}_0000.nii.gz && cp {case_folder}/segmentations/brain.nii.gz {target_lb}/{x:04d}.nii.gz'
        print(command)