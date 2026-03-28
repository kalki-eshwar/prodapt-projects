import { useAuth } from "../context/AuthContext";

function RoleBasedView({ allowedRoles, children, fallback = null }) {
  const { role } = useAuth();
  if (!allowedRoles.includes(role)) {
    return fallback;
  }

  return children;
}

export default RoleBasedView;
