def count_my_photos(directory, filetype):
    """
    Counts photos with a selected filetype from a selected directory

    :param directory: string of directory
    :param filetype: e.g. jpg png heic
    :return: number of files
    """
    count = {}
    phs = os.listdir(directory)
    for photo in phs:
        if photo.endswith(filetype):
            count += 1

    print(count)