import React from "react";

function FormError({ message }) {
  return <div className="text-sm py-2 text-red-500">{message}</div>;
}

export default FormError;
