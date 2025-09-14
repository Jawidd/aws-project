# Week 0 — Billing and Architecture

## How this project is different:
## 🔒 Security Best Practices used
### Data Protection Strategy
- **Zero Hardcoded Secrets**: Maximum effort taken to avoid hardcoding sensitive data (email addresses, AWS account IDs, credentials, etc.)
- **Encrypted Storage**: When sensitive data is required for services like notifications, all information is stored in AWS Systems Manager Parameter Store using encrypted SecureString format
- **Dynamic References**: CloudFormation templates use intrinsic functions and dynamic references instead of hardcoded values
- **Environment Agnostic**: Templates work across different AWS accounts without modification

### Implementation Details
- ✅ Email addresses stored as encrypted SSM parameters
- ✅ Templates use `{{resolve:ssm-secure:/path/to/parameter}}` syntax for sensitive data
- ✅ Configuration values parameterized for multi-environment support  
- ✅ IAM policies use AWS pseudo parameters (`${AWS::AccountId}`, `${AWS::Region}`)
- ✅ No credentials or personal data in source code

### Benefits
- **Security**: Encrypted storage of sensitive information
- **Maintainability**: Easy to update configurations without code changes
- **Reusability**: Templates work across different environments and accounts
- **Compliance**: Follows AWS security best practices
