import { isRouteErrorResponse, useRouteError } from "react-router-dom";

export default function RootError() {
    const error = useRouteError();

    // --- 1. React Router known errors (redirects, thrown responses) ---
    if (isRouteErrorResponse(error)) {
        return (
            <div className="Error-Container">
                <h1>{error.status} — {error.statusText}</h1>
                <p>{error.data?.message || "Something went wrong."}</p>
            </div>
        );
    }

    // --- 2. API / loader / action JavaScript errors ---
    if (error instanceof Error) {
        return (
            <div className="Error-Container">
                <h1>Unexpected Error</h1>
                <p>{error.message}</p>
                <pre style={{ color: "grey" }}>{error.stack}</pre> {/* optional */}
            </div>
        );
    }

    // --- 3. Unknown Error type (fallback) ---
    return (
        <div className="Error-Container">
            <h1>Something went wrong</h1>
            <p>Unknown error occurred.</p>
        </div>
    );
}
