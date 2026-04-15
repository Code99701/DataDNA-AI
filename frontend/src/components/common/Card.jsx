export default function Card({ children }) {
  return (
    <div style={{
      background: "#1e293b",
      padding: "20px",
      borderRadius: "10px",
      marginTop: "20px"
    }}>
      {children}
    </div>
  );
}