import React from "react";

export default function Input({
    type = "text",
    value,
    onChange,
    placeholder,
    className = "",
    ...rest
}) {
    return (
        <input
            type={type}
            value={value}
            onChange={onChange}
            placeholder={placeholder}
            className={`input ${className}`}
            {...rest}
        />
    );
}
