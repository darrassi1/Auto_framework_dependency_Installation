<script>
  import { onMount } from 'svelte';
  import { executeNotebookapi } from "../api.js";

  let userInput = '';
  let htmlOutput = '';

  async function executeNotebook() {
    htmlOutput = await executeNotebookapi(userInput);
  }
</script>

<main>
  <div class="input-section">
    <textarea bind:value={userInput} placeholder="Enter your code here..."></textarea>
    <button on:click={executeNotebook}>Execute</button>
  </div>
  <div class="output-section">
    <div class="output">
      {@html htmlOutput}
    </div>
  </div>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    height: 100vh; /* Full viewport height */
    font-family: Arial, sans-serif;
  }

  .input-section {
    flex: 0 1 auto; /* Adjusts based on content, but doesn't grow */
    padding: 1em;
    max-width: 600px;
    margin: 0 auto;
    box-sizing: border-box;
  }

  textarea {
    width: 100%;
    height: 100px;
    padding: 0.5em;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 1em;
    resize: vertical;
  }

  button {
    margin-top: 1em;
    padding: 0.5em 1em;
    border: none;
    border-radius: 4px;
    background-color: #007BFF;
    color: white;
    cursor: pointer;
    font-size: 1em;
  }

  button:hover {
    background-color: #0056b3;
  }

  .output-section {
    flex: 1 1 auto; /* Takes remaining space, grows if needed */
    overflow-y: auto; /* Ensures the section can scroll */
    padding: 1em;
    background-color: #f9f9f9;
    box-sizing: border-box;
  }

  .output {
    padding: 1em;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #fff;
    box-sizing: border-box;
    font-size: 1em;
    line-height: 1.5em;
    white-space: pre-wrap; /* Ensure preformatted text is wrapped */
    word-wrap: break-word; /* Ensure long words are wrapped */

  }
</style>
