# python-executor

使用阿里云函数计算（Aliyun Function Compute）搭建的一个在线 Python 代码执行器

## 部署步骤

### 创建函数

前往阿里云，免费开通函数计算服务（选择后付费模式），创建服务和函数，语言选择 `python3`。

### 自动部署

使用 GitHub Action 可以将项目自动部署至函数计算。使用时需配置以下的环境变量：

- `FUNCTION_TRIGGER_URL`: 函数触发器路径
- `ACCESS_KEY_ID`: 阿里云账号的 Access Key ID
- `ACCESS_KEY_SECRET`：阿里云账号的 Access Key 密钥

### 环境变量

在“概览”页面，可以设置环境变量。推荐将 `TZ` 设置为 `Asia/Shanghai`，使得代码中读取到的时间为东八区时间（默认为 UTC 时间）。

## 安全性

阿里云函数计算每次运行都会创建一个新的容器，因此不太需要担心运行危险的代码造成的环境破坏。但是要注意如果用户提交的代码访问公网会产生一定的费用，因此我建议关闭函数计算的公网访问功能。

## 费用说明

阿里云函数计算的后付费模式拥有每个月 100 万次的免费调用次数和每个月 40 万（GB·秒）的计算资源，在小规模应用上几乎不可能需要付费。日志服务（SLS）也可以选择开启，但一定要注意把日志活跃 Shard 数量由 2 改为 1，否则会每个月产生几毛钱的费用。

如果想要完全免费地部署一个应用，我的建议是前后端分离，使用阿里云对象存储部署前端页面，使用阿里云函数计算部署后端，使用阿里云表格存储作为数据库（注意表格存储不支持 JOIN 和事务），这些在使用量较小的情况下都是免费或费用极低的。
