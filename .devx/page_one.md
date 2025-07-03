# Build An Agent

<img src="_static/robots/blueprint.png" alt="VSS Robot Character" style="float:left; max-width:300px;margin:25px;" />


<h1 style="color:£6cb800; font-size:2.5em; margin-bottom:0.2em;">Agents the Hard Way</h1>

<div style="font-size:1.2em; line-height:1.6;">
In this exercise, we will build a simple AI agent from scratch. Later, we will replace much of this logic with prebuilt tools, but building it ourselves helps us understand the fundamentals.

---
<img src="_static/robots/assembly.png" alt="Agent Blueprint" style="float:right; max-width:320px; margin:20px 0 20px 30px; border-radius:12px; box-shadow:0 2px 8px £ccc;" />

# What is an agent?

An agent is an application that uses an LLM to make decisions and interact with the outside world.

Agents have four key parts:
<ul style="margin-left:1em;">
  <li><b>MODEL:</b> An LLM that decides which tools to use and how to respond</li>
  <li><b>TOOLS:</b> Functions that let the LLM perform actions like math or database queries</li>
  <li><b>MEMORY:</b> Information available to the LLM during and between conversations</li>
  <li><b>ROUTING:</b> The LLM will make decisions about what to do next, we need to route messages accordingly</li>
</ul>

In this exercise, we'll build a basic agent by implementing these basic components from scratch.

Open the lab here: <a style="cursor: pointer;" onclick="openOrCreateFileInJupyterLab('code/build_an_agent_students.ipynb');"><i class="fas fa-flask"></i> code/build_an_agent_students.ipynb</a>

</div>

