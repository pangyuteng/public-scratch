ARG ADDITIONAL_PRODUCTS="Computer_Vision_Toolbox Curve_Fitting_Toolbox GPU_Coder Image_Processing_Toolbox MATLAB_Coder MATLAB_Compiler MATLAB_Compiler_SDK Control_System_Toolbox Database_Toolbox System_Identification_Toolbox"
ARG MATLAB_RELEASE=R2024a

FROM mathworks/matlab:$MATLAB_RELEASE
ARG MATLAB_RELEASE
ARG ADDITIONAL_PRODUCTS



# By default, the MATLAB container runs as user "matlab". To install mpm dependencies, switch to root.
USER root

# Install mpm dependencies
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install --no-install-recommends --yes \
        wget \
        ca-certificates \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*


# Switch to user matlab, and pass in $HOME variable to mpm,
# so that mpm can set the correct root folder for the support packages.
WORKDIR /tmp
USER matlab
RUN wget -q https://www.mathworks.com/mpm/glnxa64/mpm \
    && chmod +x mpm \
    && EXISTING_MATLAB_LOCATION=$(dirname $(dirname $(readlink -f $(which matlab)))) \
    && sudo HOME=${HOME} ./mpm install \
        --destination=${EXISTING_MATLAB_LOCATION} \
        --release=${MATLAB_RELEASE} \
        --products ${ADDITIONAL_PRODUCTS} \
    || (echo "MPM Installation Failure. See below for more information:" && cat /tmp/mathworks_root.log && false) \
    && sudo rm -rf mpm /tmp/mathworks_root.log

# The following environment variables allow MathWorks to understand how this MathWorks
# product is being used. This information helps us make MATLAB even better.
# Your content, and information about the content within your files, is not shared with MathWorks.
# To opt out of this service, delete the environment variables defined in the following line.
# See the Help Make MATLAB Even Better section in the accompanying README to learn more:
# https://github.com/mathworks-ref-arch/matlab-dockerfile#help-make-matlab-even-better
ENV MW_DDUX_FORCE_ENABLE=true MW_CONTEXT_TAGS=$MW_CONTEXT_TAGS,MATLAB:TOOLBOXES:DOCKERFILE:V1


ARG GROUPID
ARG USERID
ARG USERNAME

USER root
RUN groupadd -g ${GROUPID} mygroup
RUN useradd --no-log-init -u ${USERID} -g 1000 -s /bin/bash -md /home/${USERNAME} ${USERNAME}
RUN usermod -a -G ${GROUPID} ${USERNAME}
RUN echo "${USERNAME} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${USERNAME}
RUN chmod 0440 /etc/sudoers.d/${USERNAME}

USER ${USERNAME}
WORKDIR /home/${USERNAME}
RUN mkdir -p /home/${USERNAME}/Documents/MATLAB

ENTRYPOINT [""]
CMD [""]
