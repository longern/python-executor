# python-executor

使用阿里云函数计算（Aliyun Function Compute）搭建的一个在线 Python 代码执行器，带你几乎零成本体验 Serverless 技术。

## 部署步骤

### 创建函数

前往阿里云，免费开通函数计算服务（选择后付费模式），创建服务和函数，语言选择 `python3`。

### 自动部署

使用 GitHub Action 可以将项目自动部署至函数计算。使用时需配置以下的环境变量：

- `FUNCTION_COMPUTE_ARN`: 函数 ARN（在函数计算控制台右上角复制）
- `ACCESS_KEY_ID`: 阿里云账号的 Access Key ID
- `SECRET_ACCESS_KEY`：阿里云账号的 Access Key 密钥

### 环境变量

在“概览”页面，可以设置环境变量。推荐将 `TZ` 设置为 `Asia/Shanghai`，使得代码中读取到的时间为东八区时间（默认为 UTC 时间）。

## 调用方法

向部署后的 URL 发送 POST 请求，请求体格式为
```
{
    "source": <Your source code here>,
    "input": <Your standard input here>
}
```

## 安全性

阿里云函数计算每次运行都会创建一个新的容器，因此不需要担心运行危险的代码造成的环境破坏。但是要注意如果用户提交的代码访问公网会产生一定的费用，因此建议关闭函数计算的公网访问功能。
