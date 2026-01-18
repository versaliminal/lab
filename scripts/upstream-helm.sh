#!/bin/bash
MANIFEST_FILE="config/kubernetes/upstream-helm/manifest.yaml"
INDENTER="paste /dev/null -"

function install_from_repo() {
    CFG_FILE="${1}"
    REPO_NAME="${2}"
    YAML_CONTENT="${3}"

    echo -e "\nInstalling required CRDs..."
    echo "--------------------------------"
    for url in $(echo "${YAML_CONTENT}" | yq ".crds[]"); do
        echo "  - Applying CRD from ${url}..."
        kubectl apply -f ${url} | ${INDENTER}
    done

    echo -e "\nInstalling charts from upstream manifest..."
    echo "--------------------------------"
    REPO_URL=$(echo "${YAML_CONTENT}" | yq '.url')
    REPO_VERSION=$(echo "${YAML_CONTENT}" | yq '.version')
    REPO_VARS_FILE=$(echo "${YAML_CONTENT}" | yq '.vars')

    echo "  - Adding Helm repo ${REPO_NAME} from ${REPO_URL}..."
    helm repo add ${REPO_NAME} ${REPO_URL} | ${INDENTER}

    echo "  - Installing Helm chart ${REPO_NAME} version ${REPO_VERSION}..."
    helm upgrade --install "${REPO_NAME}" "${REPO_NAME}/${REPO_NAME}" --version "${REPO_VERSION}" \
     -n "infra" --create-namespace -f "config/kubernetes/upstream-helm/${REPO_VARS_FILE}" | ${INDENTER}
}


if [[ -z "${1}" ]] || [[ -z "${2}" ]] || [[ -z "${3}" ]]; then
    echo "Require arguments: <install|uninstall> <chart|osi> <name>"
    exit 1
fi

if [[ "${2}" == "chart" ]]; then
    YAML=$(yq ".helm_repos.${3}" ${MANIFEST_FILE})
    if [[ "${1}" == 'install' ]]; then
        install_from_repo "${MANIFEST_FILE}" "${3}" "${YAML}"
    else
        echo -e "\nUninstalling Helm chart ${3}..."
        echo "--------------------------------"
        helm uninstall "${3}" -n "infra" | ${INDENTER}
    fi

elif [[ "${2}" == "osi" ]]; then
    echo "Not implemented yet"
fi