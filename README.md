# ODH Schemas API

This repo contains the code for a Schemas API used within the ODH project, which can be used to server Topic schemas.

## Using the function
~~~bash
curl \
    --silent \
    --request GET \
    --header "Content-Type: application/json" \
    --header "Authorization: bearer ${identity_token}" \
    https://europe-west1-"${CONFIG_PROJECT}".cloudfunctions.net/"${CONFIG_PROJECT}"-schemasapi/schemas/[TOPIC_NAME]")
~~~

## Retrieve an identity token in a Cloud Build
Check below the code sample to get an identity token with a Cloud Build

~~~bash
AUDIENCE="https://europe-west1-${CONFIG_PROJECT}.cloudfunctions.net/${CONFIG_PROJECT}-schemasapi"
SERVICE_ACCOUNT="schemasapi@${CONFIG_PROJECT}.iam.gserviceaccount.com"

token=$(curl \
    --silent \
    --request POST \
    --header "content-type: application/json" \
    --header "Authorization: Bearer $(gcloud auth print-access-token)" \
    --data "{\"audience\": \"${AUDIENCE}\" }" \
    "https"://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${SERVICE_ACCOUNT}:generateIdToken")

identity_token=$(echo "${token}" | python3 -c "import sys, json; j=json.loads(sys.stdin.read()); print(j['token'])")
~~~
