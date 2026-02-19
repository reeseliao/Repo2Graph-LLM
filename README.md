
# 🧠 Repo2Graph-LLM: Automated Codebase Architecture Mapping

![Graph View Screenshot](graph.png)
*(Example: Generating an interlinked Knowledge Graph for the OpenCV Core Module)*

##  Overview
**Repo2Graph-LLM** is a generic static analysis pipeline designed to reverse-engineer massive, legacy C/C++ codebases. 
By leveraging **Local Large Language Models (LLMs)**, it automatically parses source code, extracts semantic logic, and generates an interlinked Knowledge Graph in **Obsidian**. 

Instead of drowning in thousands of header files, this tool provides developers with a "bird's-eye view" of class dependencies and system architecture in minutes.

##  Why I Built This?
This tool was originally developed as a preparation strategy for **Google Summer of Code (GSoC) 2026**. Modern open-source projects have steep learning curves. I needed a way to rapidly understand complex architectures without compromising data privacy (hence the 100% local LLM approach).

**Key Features:**
*  **Privacy-First:** Powered by **Ollama** and **Gemma-2**. No proprietary code is ever sent to the cloud.
*  **Bi-directional Linking:** Automatically wraps key components (e.g., classes, structs) in `[[Wiki-Links]]` to build an Obsidian graph.
*  **Noise Reduction:** Intelligently filters out tests, samples, and 3rd-party binaries to focus strictly on core logic.

##  The OpenCV Stress Test (Benchmark)
To prove the tool's capability on industry-standard C++ code, I benchmarked it against the **OpenCV `modules/core` directory**.

* **Target:** 148 complex C++ header files (`.hpp`).
* **Hardware:** Single consumer-grade GPU.
* **Result:** Processed the entire core architecture in **< 90 minutes**. 
* **Insight:** The generated knowledge graph successfully highlighted the extreme centrality of the `cv::Mat` memory structure and mapped out the asynchronous computation logic (`async.hpp`) with zero human intervention.

##  Tech Stack
* **Language:** Python 3.10+
* **Local Inference:** Ollama 
* **Model:** Gemma-2 (9B) 
* **Visualization:** Obsidian (Markdown engine)

##  Quick Start

### 1. Prerequisites
Install [Ollama](https://ollama.com) and pull a local model:
```bash
ollama run gemma2
