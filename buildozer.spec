name: Build APK

on:
  workflow_dispatch:

jobs:
  build:
    name: Build Android APK
    runs-on: ubuntu-22.04

    steps:
      - name: Baixar projeto
        uses: actions/checkout@v5

      - name: Configurar Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.11"

      - name: Instalar dependências
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            git \
            zip \
            unzip \
            openjdk-17-jdk \
            autoconf \
            automake \
            libtool \
            pkg-config \
            zlib1g-dev \
            libncurses5-dev \
            libncursesw5-dev \
            cmake \
            libffi-dev \
            libssl-dev

      - name: Instalar Buildozer
        run: |
          python -m pip install --upgrade pip
          pip install buildozer
          pip install "cython==0.29.36"

      - name: Gerar APK
        run: |
          buildozer android debug

      - name: Disponibilizar APK
        uses: actions/upload-artifact@v4
        with:
          name: nicolas-optimizer-mobile
          path: bin/*.apk
