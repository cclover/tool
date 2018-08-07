#!/usr/bin/python
#-*- encoding=utf8 -*-


'''
检查Android工程中图片大小和重复图片
v1.0.0
chengchao128@gmail.com
'''

import os,sys
import hashlib

#const
IMAGE_DIR = "drawable"
IMAGE_EXT = (".jpg", ".jpeg",".png",)
BUILD_FILE_DIR = "build/intermediates"
IMAGE_BIG_SIZE = 0*1024

OUTPUT_FILE = "image_scan_result.log"

imagesList = []
sameFileList = {}
                                           
def md5sum(filename):             
    myhash = hashlib.md5()
    f = file(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

# check the folder is android image folder
def isImageFolder(dirPath):

    if not os.path.isdir(dirPath):
        return False
    dirName = os.path.dirname(dirPath)
    if dirName.startswith(IMAGE_DIR):
        return True
    return False

# check the file is image
def isImageFile(filePath):
    
    extName = os.path.splitext(filePath)[1].lower()
    if extName in IMAGE_EXT:
        return True
    return False


def checkFileSize(filePath):

    #image in build dir
    if BUILD_FILE_DIR in filePath:
        return
    
    if isImageFile(filePath):

        #md5
        fileMd5 = md5sum(filePath)
        size = os.path.getsize(filePath)
        if not sameFileList.has_key(fileMd5):
            sameFileList.setdefault(fileMd5,[(filePath,size)])
        else:
            fileList = sameFileList.get(fileMd5)
            fileList.append((filePath,size))

        # print filePath
        if size > IMAGE_BIG_SIZE:
            imagesList.append((filePath, size))


# recursion all folder to find the image folder
def recursionFolder(path):
    
    #need dir
    if not os.path.isdir(path):
        return

    #current is Image dir or not
    if isImageFolder(path):
        for filePath in os.walk(path):
            checkFileSize(filePath)
    else:
        for dirpath,dirnames,filenames in os.walk(path):
            for name in filenames:
                fullpath=os.path.join(dirpath,name)
                if IMAGE_DIR in fullpath:
                    checkFileSize(fullpath)



def outputResult(filePath):

    f = file(filePath,'w')

    #write the big image to file
    imagesList.sort(key=lambda item:item[1],reverse=True)
    print >> f, 'The big image file list (siez > {0}K):'.format(IMAGE_BIG_SIZE/1024)
    total = 0
    count = 0
    for filePath,size in imagesList:
        count += 1
        total += size
        outSize = size/1024
        if outSize > 0:
            print >> f,  'Image size {0}K: {1}'.format(outSize, filePath)
        else:
            print >> f,  'Image size {0}B: {1}'.format(size, filePath)

    print >> f, ' '       
    print >> f, 'Total count:{0}, size:{1}M'.format(count, total/1024/1024)

    print >> f, ' '
    print >> f, '=================================================================='
    print >> f, 'The same image file list:'
    for key,value in sameFileList.items(): 
        length = len(value)
        if length > 1:

            size = value[1][1]
            total = length + size
            if size >= 1024:
                print >> f, "Hash:{0}, ({1}*{2}K)".format(key, length, size/1024)
            else:
                print >> f, "Hash:{0}, ({1}*{2}B)".format(key, length, size)
            for path,size in value:
                print >> f, '    {0}'.format(path)
            print >> f, ' '
    
    f.close()
    


#current dir
pwd = os.path.dirname(os.path.realpath(__file__))
print 'Start to chcek all image file size under ' + pwd
recursionFolder(pwd)
result = os.path.join(pwd, OUTPUT_FILE)
outputResult(result)


    






