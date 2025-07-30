const API_URL = "http://54.174.97.84:5000";  // Replace with your EC2 IP if different

// Upload file to backend
async function uploadFile() {
  const input = document.getElementById("fileInput");
  const file = input.files[0];

  if (!file) {
    alert("Please select a file to upload.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_URL}/upload`, {
      method: "POST",
      body: formData
    });
    const result = await res.json();
    alert(result.message || result.error);
    listFiles();  // Refresh file list
  } catch (err) {
    console.error("Upload error:", err);
    alert("Error uploading file.");
  }
}
// Fetch and display file list
async function listFiles() {
  try {
    const res = await fetch(`${API_URL}/files`);
    const data = await res.json();
    const list = document.getElementById("fileList");
    list.innerHTML = "";

    if (!data.files || data.files.length === 0) {
      list.innerHTML = "<li>No files found.</li>";
      return;
    }

    data.files.forEach(file => {
      const li = document.createElement("li");
      li.textContent = file;

      const delBtn = document.createElement("button");
      delBtn.textContent = "Delete";
      delBtn.style.marginLeft = "10px";
      delBtn.onclick = async () => {
        await fetch(`${API_URL}/delete/${file}`, { method: "DELETE" });
        listFiles();
      };

      li.appendChild(delBtn);
      list.appendChild(li);
});
  } catch (err) {
    console.error("Error fetching files:", err);
    const list = document.getElementById("fileList");
    list.innerHTML = "<li>Error fetching files.</li>";
  }
}

// Run when page loads
document.addEventListener("DOMContentLoaded", () => {
  listFiles();
  document.getElementById("uploadBtn").addEventListener("click", uploadFile);
});
