FROM tensorflow/tensorflow:2.21.0 AS mybuilder

ENV DEBIAN_FRONTEND=noninteractive
ENV MYPATH=/usr/local
ENV MYLIBPATH=/usr/local/lib

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
    autotools-dev \
    build-essential \
    ca-certificates \
    software-properties-common \
    vim git wget curl \
    make \
    cmake \
    g++ \
    libbz2-dev \
    libosmesa6-dev \
    libtiff5-dev \
    libpng-dev \
    libjpeg-dev \
    libgif-dev \
    libxml2-dev \
    libssl-dev \
    zlib1g-dev \
    libwrap0-dev \
    libssl-dev && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /opt

FROM mybuilder AS vtkitk
# build vtk with osmesa ref https://dev.pyvista.org/extras/building_vtk.html
WORKDIR /opt/sources
RUN mkdir -p /opt/sources/vtk
RUN wget --quiet --no-check-certificate https://gitlab.kitware.com/vtk/vtk/-/archive/v9.6.0/vtk-v9.6.0.tar.gz -O vtk.tar.gz && \
    tar -xzf vtk.tar.gz -C /opt/sources/vtk --strip-components 1
WORKDIR /opt/sources/vtk
RUN mkdir build
WORKDIR /opt/sources/vtk/build
RUN cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=$MYPATH \
    -DBUILD_SHARED_LIBS=ON \
    -DVTK_BUILD_TESTING=OFF \
    -DVTK_BUILD_DOCUMENTATION=OFF \
    -DVTK_BUILD_EXAMPLES=OFF \
    -DVTK_OPENGL_HAS_EGL=False \
    -DVTK_OPENGL_HAS_OSMESA=True \
    -DVTK_USE_COCOA=FALSE \
    -DVTK_USE_X=FALSE \
    -DVTK_DEFAULT_RENDER_WINDOW_HEADLESS=True \
    -DVTK_MODULE_ENABLE_VTK_PythonInterpreter:STRING=NO \
    -DVTK_WHEEL_BUILD=OFF \
    -DVTK_WRAP_PYTHON=ON && \
    make -j"$(nproc)" && make install -j"$(nproc)"

# build itk
WORKDIR /opt/sources
RUN mkdir -p /opt/sources/itk
RUN wget --quiet --no-check-certificate https://github.com/InsightSoftwareConsortium/ITK/releases/download/v5.4.6/InsightToolkit-5.4.6.tar.gz -O itk.tar.gz && \
    tar -xzf itk.tar.gz -C /opt/sources/itk --strip-components 1
WORKDIR /opt/sources/itk
RUN mkdir build
WORKDIR /opt/sources/itk/build
RUN cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=$MYPATH \
    -DBUILD_DOXYGEN=OFF \
    -DBUILD_EXAMPLES=OFF \
    -DBUILD_SHARED_LIBS=OFF \
    -DITK_DYNAMIC_LOADING=OFF \
    -DBUILD_TESTING=OFF \
    -DCMAKE_BACKWARDS_COMPATIBILITY=3.1 \
    -DITK_USE_KWSTYLE=OFF \
    -DITK_BUILD_ALL_MODULES=ON \
    -DModule_ITKVtkGlue=ON -DITK_USE_REVIEW=ON && \
    make -j"$(nproc)" && make install -j"$(nproc)"

RUN tar cvzf usrlocal.tar.gz /usr/local

FROM mybuilder AS others
# build zlib
WORKDIR /opt/sources
RUN mkdir -p /opt/sources/zlib
RUN wget --quiet https://zlib.net/fossils/zlib-1.2.11.tar.gz -O zlib.tar.gz && \
    tar -xzf zlib.tar.gz -C /opt/sources/zlib --strip-components 1
WORKDIR /opt/sources/zlib
RUN ./configure --prefix=$MYPATH && make -j"$(nproc)" && make install -j"$(nproc)"

# build boost
WORKDIR /opt/sources
ENV CPLUS_INCLUDE_PATH=/usr/include/python3.11
RUN mkdir -p /opt/sources/boost
RUN wget --quiet --no-check-certificate https://archives.boost.io/release/1.79.0/source/boost_1_79_0.tar.gz -O boost.tar.gz && \
     tar -xzf boost.tar.gz -C /opt/sources/boost --strip-components 1
WORKDIR /opt/sources/boost

# RUN ./bootstrap.sh --prefix=$MYPATH --with-python=python3.11 \
#     --with-libraries=python,filesystem,system,test,iostreams && \
#     ./b2 install

RUN ./bootstrap.sh --prefix=$MYPATH \
    --with-libraries=filesystem,system,test,iostreams && \
    ./b2 install

# build dcmtk
WORKDIR /opt/sources
RUN mkdir -p /opt/sources/dcmtk
RUN wget --quiet https://github.com/DCMTK/dcmtk/archive/DCMTK-3.7.0.tar.gz -O dcmtk.tar.gz && \
    tar -xzf dcmtk.tar.gz -C /opt/sources/dcmtk --strip-components 1
WORKDIR /opt/sources/dcmtk
RUN mkdir build
WORKDIR /opt/sources/dcmtk/build
RUN cmake .. \
    -DCMAKE_INSTALL_PREFIX=$MYPATH \
    -DCMAKE_LIBRARY_PATH=$MYLIBPATH \
    -DDCMTK_FORCE_FPIC_ON_UNIX:BOOL=ON && \
    make -j"$(nproc)" && make install -j"$(nproc)"

# build gdcm
WORKDIR /opt/sources
RUN mkdir -p /opt/sources/gdcm
RUN wget --quiet https://github.com/malaterre/GDCM/archive/v3.2.7.tar.gz -O gdcm.tar.gz && \
    tar -xzf gdcm.tar.gz -C /opt/sources/gdcm --strip-components 1
WORKDIR /opt/sources/gdcm
RUN mkdir build
WORKDIR /opt/sources/gdcm/build
RUN cmake .. \
    -DCMAKE_INSTALL_PREFIX=$MYPATH \
    -DCMAKE_LIBRARY_PATH=$MYLIBPATH \
    -DGDCM_BUILD_APPLICATIONS=1 \
    -DGDCM_BUILD_SHARED_LIBS=1 && \
    make -j"$(nproc)" && make install -j"$(nproc)"

RUN tar cvzf usrlocal.tar.gz /usr/local

# 
# NOTE: to use multi stage building...just use tar to maintain path
# ref https://stackoverflow.com/a/53285818/868736
# 

FROM mybuilder AS base
ENV MAIN_LIBRARYDIR=/usr/local/lib
ENV LD_LIBRARY_PATH=$MAIN_LIBRARYDIR

WORKDIR /
COPY --from=vtkitk /opt/sources/usrlocal.tar.gz /usrlocal-vtkitk.tar.gz
COPY --from=others /opt/sources/usrlocal.tar.gz /usrlocal-others.tar.gz
RUN tar xfz /usrlocal-vtkitk.tar.gz && tar xfz /usrlocal-others.tar.gz && \
    rm /usrlocal-vtkitk.tar.gz /usrlocal-others.tar.gz

RUN python -m pip install --upgrade pip
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /
RUN tar cvzf include.tar.gz /usr/local/include
RUN tar \
    --exclude=/usr/local/lib/cmake \
    --exclude=/usr/local/lib/pkgconfig \
    --exclude=/usr/local/lib/python3.11 \
    -cvzf lib.tar.gz \
    /usr/local/lib
RUN tar -cvzf gdcm.tar.gz /usr/local/bin/gdcm*

# WORKDIR /opt
