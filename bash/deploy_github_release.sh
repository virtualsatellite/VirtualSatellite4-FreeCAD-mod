#!/bin/bash

#/*******************************************************************************
# * Copyright (c) 2020 German Aerospace Center (DLR), Simulation and Software Technology, Germany.
# *
# * This program and the accompanying materials are made available under the
# * terms of the Eclipse Public License 2.0 which is available at
# * http://www.eclipse.org/legal/epl-2.0.
# *
# * SPDX-License-Identifier: EPL-2.0
# *******************************************************************************/

# --------------------------------------------------------------------------
# This script is used to control the deployment to github release and to
# sourceforge
# --------------------------------------------------------------------------

# turn on failing
set -e

# Store the name of the command calling from commandline to be properly
# displayed in case of usage issues
COMMAND=$0
__DIR=$(dirname "$0")

# this method gives some little usage info
printUsage() {
	echo "usage: ${COMMAND} -p [development|integration|release] -r <ref> -t <token> -s <repository> -g <sha>"
	echo ""
	echo "Options:"
	echo " -p, --profile <profile>       The name of the maven profile to be deployed."
	echo " -r, --ref <ref>               The GitHub ref on which the deploy is issued"
	echo " -t, --token <token>           The token for being able to access the GitHub Repository."
	echo " -s, --repository <repository> The repository in which to create the tags and releases."
	echo " -g, --sha <sha>               The SHA sum of the commit from which the build has been triggered."
	echo ""
	echo "Copyright by DLR (German Aerospace Center)"
}

createOrMoveTag() {
	echo "About to create the tags"
	if [[ $BUILD_PROFILE == "development" ]] || \
	   [[ $BUILD_PROFILE == "integration" ]]; then
		TAG_NAME=${BUILD_PROFILE}_snapshot
		echo "Creating the $TAG_NAME tag in $GITHUB_REPOSITORY"
		
		git tag -f "$TAG_NAME"
		git remote add github-repo "https://$GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git"
		git push -f github-repo "$TAG_NAME"
		git remote remove github-repo
		
		echo "Created or moved $TAG_NAME tag"
		
	else
		echo "Not creating or moving any tag"
	fi
}

# TODO: version number
deployToGitHubReleases() {
	echo "About to deploy to the GitHub Release"
	if [[ $BUILD_PROFILE == "development" ]] || \
	   [[ $BUILD_PROFILE == "integration" ]]; then
		TAG_NAME=${BUILD_PROFILE}_snapshot
		echo "Uploading development/integration to $TAG_NAME tag in $GITHUB_REPOSITORY ..."
		
		"${__DIR}/github_release_api.sh" -t "$GITHUB_TOKEN" -c delete -r "$TAG_NAME"
		"${__DIR}/github_release_api.sh" -t "$GITHUB_TOKEN" -c create -r "$TAG_NAME" -d "Development/Integration build on latest commit by Github Actions CI - $GITHUB_REPOSITORY ($GITHUB_SHA) - $(date +'%F %T %Z'). This release is subject to constant change."
		"${__DIR}/github_release_api.sh" -t "$GITHUB_TOKEN" -c multi -r "$TAG_NAME" -p "*.zip" -dir deploy/unsecured
		"${__DIR}/github_release_api.sh" -t "$GITHUB_TOKEN" -c multi -r "$TAG_NAME" -p "*.tar.gz" -dir deploy/unsecured

		echo "Uploaded to $TAG_NAME tag"
	
	elif [[ $BUILD_PROFILE == "release" ]]; then
		TAG_NAME=${GITHUB_REF#refs/*/}
		echo "Uploading release to $TAG_NAME tag in $GITHUB_REPOSITORY ..."
		
		"${__DIR}/github_release_api.sh" -t "$GITHUB_TOKEN" -c patch -r "$TAG_NAME" -d "Release build for tag ($TAG_NAME) by Github Actions CI - $GITHUB_REPOSITORY ($GITHUB_SHA) - $(date +'%F %T %Z'). This is a stable Release."
		"${__DIR}/github_release_api.sh" -t "$GITHUB_TOKEN" -c multi -r "$TAG_NAME" -p "*.zip" -dir ../deploy/secured
		"${__DIR}/github_release_api.sh" -t "$GITHUB_TOKEN" -c multi -r "$TAG_NAME" -p "*.tar.gz" -dir ../deploy/secured

		echo "Uploaded to $TAG_NAME tag"
		
	else
		echo "Not deploying to GitHub Releases"
	fi
}


# process all command line arguments
while [ "$1" != "" ]; do
    case $1 in
        -p | --profile )        shift
                                BUILD_PROFILE=$1
                                ;;
        -r | --ref )            shift
                                GITHUB_REF=$1
                                ;;
        -t | --token )          shift
                                GITHUB_TOKEN=$1
                                ;;
        -s | --repository )     shift
                                GITHUB_REPOSITORY=$1
                                ;;
        -g | --sha )            shift
                                GITHUB_SHA=$1
                                ;;
        -h | --help )           printUsage
                                exit
                                ;;
        * )                     printUsage
                                exit 1
    esac
    shift
done

case $BUILD_PROFILE in
    development )       ;;
    integration )       ;;
    release )           ;;
    * )                 printUsage
                        exit 1
esac

if [ -z "$GITHUB_REF" ]; then
   echo "ERROR - GitHub REF is not provided."
   printUsage
   exit 1
fi

if [ -z "$GITHUB_TOKEN" ]; then
   echo "ERROR - GitHub Token for writing to the repository is not provided."
   printUsage
   exit 1
fi

if [ -z "$GITHUB_REPOSITORY" ]; then
   echo "ERROR - There is not GitHub repository provided in which to create the tags and releases"
   printUsage
   exit 1
fi

if [ -z "$GITHUB_SHA" ]; then
   echo "ERROR - The SHA for the GitHub commit is not provided"
   printUsage
   exit 1
fi

createOrMoveTag
deployToGitHubReleases
