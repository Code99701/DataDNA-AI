export default function Button({ children, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        background: "#3b82f6",
        border: "none",
        padding: "10px 20px",
        borderRadius: "8px",
        color: "white",
        cursor: "pointer"
      }}
    >
      {children}
    </button>
  );
}