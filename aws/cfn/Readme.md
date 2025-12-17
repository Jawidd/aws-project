## Architecture Guide

Before you run any templates, be sure to create an S3 bucket(must be unique name) to contain all of our artifacts for CloudFormation.


```

aws s3 mk s3://cfn-artifacts

export CFN_BUCKET="cfn-artifacts"

gp env CFN_BUCKET="cfn-artifacts"

```




