# tool


##AndroidImageChecker
检查Android图片资源大小和重复图片的工具.


###使用
放在工程的根目录。执行命令。 

```shell
python checkImage.py
```
默认会找出当前工程中，所有drawable目录下的图片文件，按大小排序，并找出重复文件。 最终结果会输出在同一目录下的 image_scan_result.log 文件中

可以自定义要查找图片的大小和类型， 修改checkImage.py 文件对应的变量就行了。

```python

#文件类型
IMAGE_EXT = (".jpg", ".jpeg",".png",)

#要列出图片大小
IMAGE_BIG_SIZE = 0*1024

```
