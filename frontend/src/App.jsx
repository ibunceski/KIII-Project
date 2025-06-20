import { useState, useEffect } from "react";
import axios from "axios";

// const API_URL = window._env_?.VITE_API_URL || import.meta.env.VITE_API_URL || "http://localhost:8000";
const API_URL = "http://backend.grocery-app.svc.cluster.local:8000"

function App() {
    const [items, setItems] = useState([]);
    const [name, setName] = useState("");
    const [quantity, setQuantity] = useState(1);
    const [editingId, setEditingId] = useState(null);
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        fetchItems();
    }, []);

    const fetchItems = async () => {
        const res = await axios.get(`${API_URL}/api/items`);
        setItems(res.data);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!name.trim() || quantity <= 0) return;

        if (isEditing) {
            await axios.put(`${API_URL}/api/items/${editingId}`, { name, quantity });
        } else {
            await axios.post(`${API_URL}/api/items`, { name, quantity });
        }

        await fetchItems();
        resetForm();
    };

    const handleEdit = (item) => {
        setName(item.name);
        setQuantity(item.quantity);
        setEditingId(item.id);
        setIsEditing(true);
    };

    const handleDelete = async (id) => {
        await axios.delete(`${API_URL}/api/items/${id}`);
        await fetchItems();
    };

    const resetForm = () => {
        setName("");
        setQuantity(1);
        setEditingId(null);
        setIsEditing(false);
    };

    const cancelEdit = () => {
        resetForm();
    };

    return (
        <div className="container mt-5">
            <h1 className="mb-4">Grocery List</h1>
            <form onSubmit={handleSubmit} className="mb-3 d-flex gap-2">
                <input
                    type="text"
                    className="form-control"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Enter item name"
                    required
                />
                <input
                    type="number"
                    className="form-control"
                    value={quantity}
                    onChange={(e) => setQuantity(Number(e.target.value))}
                    min="1"
                    placeholder="Quantity"
                    required
                />
                <button type="submit" className="btn btn-primary">
                    {isEditing ? "Update" : "Add"}
                </button>
                {isEditing && (
                    <button type="button" className="btn btn-secondary" onClick={cancelEdit}>
                        Cancel
                    </button>
                )}
            </form>
            <ul className="list-group">
                {items.map((item) => (
                    <li key={item.id} className="list-group-item d-flex justify-content-between align-items-center">
                        <span>
                            {item.name} <span className="badge bg-secondary ms-2">x{item.quantity}</span>
                        </span>
                        <div className="btn-group">
                            <button
                                className="btn btn-sm btn-outline-primary"
                                onClick={() => handleEdit(item)}
                            >
                                Edit
                            </button>
                            <button
                                className="btn btn-sm btn-outline-danger"
                                onClick={() => handleDelete(item.id)}
                            >
                                Delete
                            </button>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;