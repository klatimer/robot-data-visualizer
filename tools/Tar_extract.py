#code originally from https://stackoverflow.com/a/30888321

def tar_extract(file_name):
    import tarfile
    if (file_name.endswith("tar.gz")):
        tar = tarfile.open(file_name, "r:gz")
        tar.extractall()
        tar.close()
    elif (file_name.endswith("tar")):
        tar = tarfile.open(file_name, "r:")
        tar.extractall()
        tar.close()

#change filename to match whatever file you want
file_name = '2013-01-10_sen.tar.gz'
extraction = tar_extract(file_name)

