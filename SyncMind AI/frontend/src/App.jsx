import React, { useEffect, useState } from "react";

const API_BASE = "/api";

export const App = () => {
  const [workspaces, setWorkspaces] = useState([]);
  const [newWorkspaceName, setNewWorkspaceName] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/workspaces`)
      .then((res) => res.json())
      .then(setWorkspaces)
      .catch(() => {});
  }, []);

  const createWorkspace = async (e) => {
    e.preventDefault();
    if (!newWorkspaceName.trim()) return;

    const res = await fetch(`${API_BASE}/workspaces`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newWorkspaceName }),
    });
    const created = await res.json();
    setWorkspaces((prev) => [...prev, created]);
    setNewWorkspaceName("");
  };

  return (
    <div style={{ fontFamily: "system-ui, -apple-system, sans-serif", padding: "2rem" }}>
      <h1>SyncMind AI</h1>
      <p>Turn student team meetings into structured tasks, owners, and deadlines.</p>

      <section style={{ marginTop: "2rem" }}>
        <h2>Workspaces</h2>
        <form onSubmit={createWorkspace} style={{ marginBottom: "1rem" }}>
          <input
            placeholder="New workspace name"
            value={newWorkspaceName}
            onChange={(e) => setNewWorkspaceName(e.target.value)}
            style={{ padding: "0.4rem 0.6rem", marginRight: "0.5rem" }}
          />
          <button type="submit">Create</button>
        </form>
        <ul>
          {workspaces.map((w) => (
            <li key={w.id}>
              {w.name} <small>({new Date(w.created_at).toLocaleString()})</small>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
};

