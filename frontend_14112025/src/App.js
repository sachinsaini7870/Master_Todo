import './App.css';
import "./assets/css/style.css"
import routes from './routes';
import { RouterProvider, createBrowserRouter } from "react-router-dom";


function App() {

  const router = createBrowserRouter(routes);

  return (
    <RouterProvider router={router} hydrate={false} />
  );
}

export default App;
