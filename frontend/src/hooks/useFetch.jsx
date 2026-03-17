import { useEffect, useState } from "react";

const useFetch = (url, type, trigger, body, token) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    if (trigger) {
      try {
        if (type === "get") {
          setLoading(true);
          const res = await fetch(url, {
            method: "get",
            headers: token
              ? {
                  "Content-type": "application/json; charset=UTF-8",
                  Authorization: `Bearer ${token}`,
                }
              : {
                  "Content-type": "application/json; charset=UTF-8",
                },
          });

          if (!res.ok) {
            const errorData = await res.json();
            setError(errorData);
            throw new Error(`Error en la solicitud: ${res.status}`);
          }
          const data = await res.json();
          if (data) {
            setData(data);
            setLoading(false);
          }
        }
        if (type === "post") {
          setLoading(true);

          const res = await fetch(url, {
            method: "POST",
            body: JSON.stringify(body),
            headers: token
              ? {
                  "Content-Type": "application/json; charset=UTF-8",
                  Authorization: `Bearer ${token}`,
                }
              : {
                  "Content-Type": "application/json; charset=UTF-8",
                },
          });

          if (!res.ok) {
            const errorData = await res.json();
            setError(errorData);
            throw new Error(`Error en la solicitud: ${res.status}`);
          }
          const data = await res.json();
          if (data) {
            setData(data);
            setLoading(false);
          }
        }
      } catch (error) {
        if (error) {
          setError(error);
          setLoading(false);
          console.log("error en la solicitud" + error);
        }
      }
    }
  };

  useEffect(() => {
    fetchData();
  }, [trigger, url]);

  return {
    data,
    error,
    loading,
  };
};

export default useFetch;
