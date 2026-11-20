# Ollama Instalation User Guide

This is a step-by-step guide on how to install Ollama and an AI model required for this project.

## 1. Update System

Before installing any software, update your OS / system

### Linux

```bash
sudo apt update
sudo apt upgrade -y
```

### Windows

```powershell
winget upgrade
```

---

## 2. Installing Ollama

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows

Download and install Ollama from:

[Ollama Downloads](https://ollama.com/download)

---

## 3. Verify Installation

Verify that the installation was successful

### Linux

```bash
ollama --version
```

### Windows

```powershell
ollama --version
```

---

## 4. Download AI Model

This is where you download the AI model. For this project, it uses mistral. If you want to use a different AI model, change the name of the AI model you are pulling in the command

### Linux & Windows

```bash
ollama pull mistral:latest
```

or

```bash
ollama pull {AI Model Name}
```

---

## 5. Verify Model Installation

Verify that the model has been installed successfully

### Linux & Windows

```bash
ollama list
```

Expected output:

```text
NAME
mistral:latest
```

or

```text
NAME
{AI Model Name}
```

---

## Test the Model

### Linux

```bash
ollama run mistral:latest
```

or

```bash
ollama run {AI Model Name}
```

### Windows

```powershell
ollama run mistral:latest
```

or

```powershell
ollama run {AI Model Name}
```

Example:

```text
>>> Hello
Hello! How can I help you?
```

To exit:

```text
/bye
```