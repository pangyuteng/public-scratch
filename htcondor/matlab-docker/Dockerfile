FROM mathworks/matlab:r2024a

ARG GROUPID
ARG USERID
ARG USERNAME

USER root
RUN groupadd -g ${GROUPID} mygroup
RUN useradd --no-log-init -u ${USERID} -g 1000 -s /bin/bash -md /home/${USERNAME} ${USERNAME}
RUN usermod -a -G ${GROUPID} ${USERNAME}
RUN echo "pteng ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${USERNAME}
RUN chmod 0440 /etc/sudoers.d/${USERNAME}

USER ${USERNAME}
WORKDIR /home/${USERNAME}
ENTRYPOINT ["/bin/run.sh"]
CMD [""]
