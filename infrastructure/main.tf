terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "create_dmv_bucket" {
  bucket        = "${var.name_prefix}-bucket"
  force_destroy = true
}
resource "aws_s3_bucket_public_access_block" "create_dmv_bucket" {
  bucket                  = aws_s3_bucket.create_dmv_bucket.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_cognito_user_pool_domain" "create_dmv" {
  domain       = replace(uuidv5("url", "urn:${var.name_prefix}"), "-", "")
  user_pool_id = aws_cognito_user_pool.create_dmv.id
}

resource "aws_cognito_user_pool" "create_dmv" {
  name                     = "${var.name_prefix}-user-pool"
  auto_verified_attributes = ["email"]
  admin_create_user_config {
    allow_admin_create_user_only = true
  }
}

resource "aws_cognito_identity_provider" "create_dmv_google" {
  user_pool_id  = aws_cognito_user_pool.create_dmv.id
  provider_name = "Google"
  provider_type = "Google"

  provider_details = {
    client_id        = var.google_client_id
    client_secret    = var.google_client_secret
    authorize_scopes = "openid email"
  }

  attribute_mapping = {
    email    = "email"
    username = "sub"
  }
}

resource "aws_cognito_resource_server" "create_dmv" {
  identifier   = local.auth_identifier
  name         = "${var.name_prefix}-resource-server"
  user_pool_id = aws_cognito_user_pool.create_dmv.id
  scope {
    scope_name        = "auth"
    scope_description = "Authenticate"
  }
}

resource "aws_cognito_user_pool_client" "create_dmv_authorization_code" {
  name                                 = "${var.name_prefix}-authorization-code"
  callback_urls                        = [local.authorization_code_oidc_redirect_url]
  user_pool_id                         = aws_cognito_user_pool.create_dmv.id
  generate_secret                      = true
  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows                  = ["code"]
  allowed_oauth_scopes                 = ["openid", "email", local.auth_oauth_scope]
  supported_identity_providers         = ["Google"]
  access_token_validity                = 24
  id_token_validity                    = 24
  refresh_token_validity               = 7
  token_validity_units {
    access_token  = "hours"
    id_token      = "hours"
    refresh_token = "days"
  }
  depends_on = [aws_cognito_identity_provider.create_dmv_google]
}