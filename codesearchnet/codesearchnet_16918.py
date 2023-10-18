def upload_files(selected_file, selected_host, only_link, file_name):
    """
    Uploads selected file to the host, thanks to the fact that
    every pomf.se based site has pretty much the same architecture.
    """
    try:
        answer = requests.post(
            url=selected_host[0]+"upload.php",
            files={'files[]':selected_file})
        file_name_1 = re.findall(r'"url": *"((h.+\/){0,1}(.+?))"[,\}]', \
            answer.text.replace("\\", ""))[0][2]
        if only_link:
            return [selected_host[1]+file_name_1, "{}: {}{}".format(file_name, selected_host[1], file_name_1)]
        else:
            return "{}: {}{}".format(file_name, selected_host[1], file_name_1)
    except requests.exceptions.ConnectionError:
        print(file_name + ' couldn\'t be uploaded to ' + selected_host[0])