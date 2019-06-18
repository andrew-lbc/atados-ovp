def boehringer_user_email_validator(data, context):
  if context['request'].channel == 'boehringer':
    email = data.get('email', '')
    if not email.endswith('@boehringer-ingelheim.com') or not email.endswith('@boehringer.com'):
      return {'email': ['Email address must be from @boehringer-ingelheim.com']}
