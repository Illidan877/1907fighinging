## GIT说明文档

Git config 配置

​	当你安装Git后首先要做的事情是设置你的用户名称和e-mail地址。这是非常重要的，因为每次Git提交都会使用该信息。它被永远的嵌入到了你的提交中。

$ git config --global user.name "wirelessqa" 

$ git config --global user.email wirelessqa.me@gmail.com 

### git初始化操作：

```python
git clone 后执行如下操作

创建本地分支
git checkout -b developer
关联远程分支
git branch --set-upstream-to=origin/developer developer
git pull/push

git branch -a 查看当前所有分支
git branch -vv 查看分支关联 - developer本地分支关联 origin/de.. 结果如下
* developer b58e2d1 [origin/developer]

```

### GIT 添加忽略文件：

​	**有时候在项目开发过程中，突然心血来潮想把某些目录或文件加入忽略规则，按照上述方法定义后发现并未生效，原因是.gitignore只能忽略那些原来没有被track的文件，如果某些文件已经被纳入了版本管理中，则修改.gitignore是无效的。那么解决方法就是先把本地缓存删除（改变成未track状态），然后再提交**

```python
命令如下：
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
```

