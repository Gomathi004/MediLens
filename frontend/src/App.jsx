import { useEffect, useState } from "react";
import {
  Show,
  SignIn,
  UserButton,
  useAuth,
} from "@clerk/react";


const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";


function App() {
  const { getToken } = useAuth();

  const [selectedFile, setSelectedFile] =
    useState(null);

  const [previewUrl, setPreviewUrl] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [result, setResult] =
    useState(null);

  const [error, setError] =
    useState("");

  const [theme, setTheme] =
    useState(() => {
      const savedTheme =
        localStorage.getItem("medilens-theme");

      return savedTheme || "light";
    });


  useEffect(() => {
    localStorage.setItem(
      "medilens-theme",
      theme
    );
  }, [theme]);


  function handleThemeToggle() {
    setTheme((currentTheme) =>
      currentTheme === "light"
        ? "dark"
        : "light"
    );
  }


  function handleFileChange(event) {
    const file =
      event.target.files?.[0];

    if (!file) {
      return;
    }

    setSelectedFile(file);
    setResult(null);
    setError("");

    const objectUrl =
      URL.createObjectURL(file);

    setPreviewUrl(objectUrl);
  }


  function handleRemove() {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    setSelectedFile(null);
    setPreviewUrl("");
    setResult(null);
    setError("");
  }


  function handleChooseAnother() {
    document
      .getElementById("medicine-image-input")
      ?.click();
  }


  async function handleAnalyze() {
    if (!selectedFile) {
      setError(
        "Please select a medicine label image first."
      );
      return;
    }

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const token =
        await getToken();

      const formData =
        new FormData();

      formData.append(
        "file",
        selectedFile
      );

      const response =
        await fetch(
          `${API_URL}/scan/`,
          {
            method: "POST",
            headers: {
              Authorization:
                `Bearer ${token}`,
            },
            body: formData,
          }
        );

      let data = null;

      try {
        data = await response.json();
      } catch {
        data = null;
      }


      if (!response.ok) {
        if (
          response.status === 422
        ) {
          setError(
            "Medicine name not detected. Please upload a closer, clearer image of the medicine label."
          );
        } else if (
          response.status === 401
        ) {
          setError(
            "Your session has expired. Please sign in again."
          );
        } else {
          setError(
            data?.detail ||
              "Something went wrong while analyzing the medicine. Please try again."
          );
        }

        return;
      }


      setResult(data);
    } catch (err) {
      console.error(
        "Medicine analysis error:",
        err
      );

      setError(
        "Unable to connect to the MediLens server. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }


  const isDark =
    theme === "dark";


  const styles = {
    page: {
      minHeight: "100vh",
      width: "100%",
      backgroundColor: isDark
        ? "#111827"
        : "#f5f7fb",
      color: isDark
        ? "#f9fafb"
        : "#0f2747",
      transition:
        "background-color 0.25s ease, color 0.25s ease",
    },

    header: {
      width: "100%",
      boxSizing: "border-box",
      backgroundColor: isDark
        ? "#1f2937"
        : "#ffffff",
      borderBottom: isDark
        ? "1px solid #374151"
        : "1px solid #e5e7eb",
      padding: "20px 36px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      transition:
        "background-color 0.25s ease, border-color 0.25s ease",
    },

    brandContainer: {
      display: "flex",
      flexDirection: "column",
      gap: "4px",
    },

    brand: {
      margin: 0,
      fontSize: "26px",
      fontWeight: 700,
      color: isDark
        ? "#ffffff"
        : "#0b2545",
    },

    subtitle: {
      margin: 0,
      fontSize: "14px",
      color: isDark
        ? "#9ca3af"
        : "#6b7fa3",
    },

    headerRight: {
      display: "flex",
      alignItems: "center",
      gap: "14px",
    },

    themeButton: {
      width: "42px",
      height: "42px",
      borderRadius: "50%",
      border: isDark
        ? "1px solid #4b5563"
        : "1px solid #d9e0eb",
      backgroundColor: isDark
        ? "#374151"
        : "#f4f6fb",
      color: isDark
        ? "#fbbf24"
        : "#315efb",
      cursor: "pointer",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: "20px",
      transition:
        "all 0.25s ease",
    },

    main: {
      width: "100%",
      maxWidth: "1100px",
      margin: "0 auto",
      padding: "58px 32px 80px",
      boxSizing: "border-box",
    },

    heading: {
      margin: 0,
      fontSize: "34px",
      fontWeight: 700,
      color: isDark
        ? "#ffffff"
        : "#0b2545",
    },

    description: {
      marginTop: "10px",
      marginBottom: "34px",
      fontSize: "16px",
      color: isDark
        ? "#9ca3af"
        : "#6b7fa3",
    },

    uploadCard: {
      width: "100%",
      minHeight: "315px",
      border: isDark
        ? "2px dashed #4b5563"
        : "2px dashed #d1d9e6",
      borderRadius: "18px",
      backgroundColor: isDark
        ? "#1f2937"
        : "#ffffff",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      boxSizing: "border-box",
      padding: "35px",
      transition:
        "background-color 0.25s ease, border-color 0.25s ease",
    },

    plusCircle: {
      width: "58px",
      height: "58px",
      borderRadius: "50%",
      backgroundColor: isDark
        ? "#263c70"
        : "#eef2ff",
      color: "#315efb",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: "31px",
      marginBottom: "22px",
    },

    uploadTitle: {
      margin: 0,
      fontSize: "21px",
      fontWeight: 700,
      color: isDark
        ? "#ffffff"
        : "#0b2545",
    },

    uploadText: {
      marginTop: "12px",
      marginBottom: "28px",
      textAlign: "center",
      fontSize: "14px",
      color: isDark
        ? "#9ca3af"
        : "#6b7fa3",
    },

    primaryButton: {
      border: "none",
      borderRadius: "8px",
      backgroundColor: "#315efb",
      color: "#ffffff",
      padding: "12px 26px",
      fontSize: "14px",
      fontWeight: 600,
      cursor: "pointer",
    },

    secondaryButton: {
      border: isDark
        ? "1px solid #4b5563"
        : "1px solid #d5dbe5",
      borderRadius: "8px",
      backgroundColor: isDark
        ? "#374151"
        : "#ffffff",
      color: isDark
        ? "#f9fafb"
        : "#0b2545",
      padding: "11px 24px",
      fontSize: "14px",
      fontWeight: 600,
      cursor: "pointer",
    },

    removeButton: {
      border: "1px solid #efb0b0",
      borderRadius: "8px",
      backgroundColor: isDark
        ? "#351c1c"
        : "#ffffff",
      color: "#e04444",
      padding: "11px 24px",
      fontSize: "14px",
      fontWeight: 600,
      cursor: "pointer",
    },

    selectedCard: {
      width: "100%",
      border: isDark
        ? "2px dashed #315efb"
        : "2px dashed #315efb",
      borderRadius: "18px",
      backgroundColor: isDark
        ? "#1f2937"
        : "#ffffff",
      padding: "28px",
      boxSizing: "border-box",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      transition:
        "background-color 0.25s ease",
    },

    preview: {
      width: "230px",
      maxHeight: "240px",
      objectFit: "contain",
      borderRadius: "10px",
      boxShadow:
        "0 8px 24px rgba(0, 0, 0, 0.12)",
      marginBottom: "20px",
    },

    fileName: {
      margin: 0,
      fontSize: "20px",
      fontWeight: 700,
      color: isDark
        ? "#ffffff"
        : "#111827",
    },

    successText: {
      marginTop: "10px",
      marginBottom: "22px",
      fontSize: "14px",
      color: isDark
        ? "#9ca3af"
        : "#6b7fa3",
    },

    buttonRow: {
      display: "flex",
      gap: "12px",
      flexWrap: "wrap",
      justifyContent: "center",
    },

    analyzeButton: {
      marginTop: "18px",
      border: "none",
      borderRadius: "8px",
      backgroundColor: loading
        ? "#7184c7"
        : "#315efb",
      color: "#ffffff",
      padding: "13px 34px",
      fontSize: "14px",
      fontWeight: 600,
      cursor: loading
        ? "not-allowed"
        : "pointer",
    },

    error: {
      width: "100%",
      boxSizing: "border-box",
      marginTop: "20px",
      padding: "14px 18px",
      borderRadius: "8px",
      border: isDark
        ? "1px solid #7f3030"
        : "1px solid #f1b4b4",
      backgroundColor: isDark
        ? "#351c1c"
        : "#fff5f5",
      color: isDark
        ? "#fca5a5"
        : "#df3f3f",
      textAlign: "center",
      fontSize: "14px",
    },

    resultSection: {
      marginTop: "38px",
      width: "100%",
    },

    resultTitle: {
      marginBottom: "20px",
      fontSize: "26px",
      fontWeight: 700,
      color: isDark
        ? "#ffffff"
        : "#0b2545",
    },

    resultGrid: {
      display: "grid",
      gridTemplateColumns:
        "repeat(auto-fit, minmax(220px, 1fr))",
      gap: "16px",
    },

    resultCard: {
      backgroundColor: isDark
        ? "#1f2937"
        : "#ffffff",
      border: isDark
        ? "1px solid #374151"
        : "1px solid #e5e7eb",
      borderRadius: "12px",
      padding: "20px",
      boxSizing: "border-box",
    },

    resultLabel: {
      margin: 0,
      fontSize: "13px",
      color: isDark
        ? "#9ca3af"
        : "#71809b",
    },

    resultValue: {
      marginTop: "8px",
      marginBottom: 0,
      fontSize: "17px",
      fontWeight: 600,
      color: isDark
        ? "#ffffff"
        : "#111827",
    },

    explanationCard: {
      marginTop: "18px",
      backgroundColor: isDark
        ? "#1f2937"
        : "#ffffff",
      border: isDark
        ? "1px solid #374151"
        : "1px solid #e5e7eb",
      borderRadius: "12px",
      padding: "24px",
      lineHeight: 1.7,
    },

    explanation: {
      margin: 0,
      whiteSpace: "pre-wrap",
      fontSize: "15px",
      color: isDark
        ? "#e5e7eb"
        : "#374151",
    },

    disclaimer: {
      marginTop: "20px",
      padding: "16px",
      borderRadius: "10px",
      backgroundColor: isDark
        ? "#302c1d"
        : "#fffbea",
      border: isDark
        ? "1px solid #665b31"
        : "1px solid #f1df9b",
      color: isDark
        ? "#f3e8a8"
        : "#705c1b",
      fontSize: "13px",
      lineHeight: 1.6,
    },
  };


  return (
    <div style={styles.page}>

      <Show when="signed-out">
        <div
          style={{
            minHeight: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor:
              isDark
                ? "#111827"
                : "#f5f7fb",
          }}
        >
          <SignIn />
        </div>
      </Show>


      <Show when="signed-in">

        <header style={styles.header}>

          <div style={styles.brandContainer}>
            <h1 style={styles.brand}>
              MediLens
            </h1>

            <p style={styles.subtitle}>
              Medicine Label Simplifier
            </p>
          </div>


          <div style={styles.headerRight}>

            <button
              type="button"
              onClick={handleThemeToggle}
              style={styles.themeButton}
              title={
                isDark
                  ? "Switch to light mode"
                  : "Switch to dark mode"
              }
              aria-label={
                isDark
                  ? "Switch to light mode"
                  : "Switch to dark mode"
              }
            >
              {isDark ? "☀" : "☾"}
            </button>


            <UserButton />
          </div>

        </header>


        <main style={styles.main}>

          <h2 style={styles.heading}>
            Medicine Label Simplifier
          </h2>

          <p style={styles.description}>
            Upload a medicine label to get a
            simplified explanation.
          </p>


          {!selectedFile && (

            <div style={styles.uploadCard}>

              <div style={styles.plusCircle}>
                +
              </div>

              <h3 style={styles.uploadTitle}>
                Upload Medicine Label
              </h3>

              <p style={styles.uploadText}>
                Choose a JPG, JPEG, PNG, or WEBP
                image of your medicine label.
              </p>

              <input
                id="medicine-image-input"
                type="file"
                accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp"
                onChange={handleFileChange}
                style={{
                  display: "none",
                }}
              />

              <button
                type="button"
                onClick={() =>
                  document
                    .getElementById(
                      "medicine-image-input"
                    )
                    ?.click()
                }
                style={styles.primaryButton}
              >
                Choose Image
              </button>

            </div>
          )}


          {selectedFile && (

            <div style={styles.selectedCard}>

              <img
                src={previewUrl}
                alt="Selected medicine label"
                style={styles.preview}
              />

              <h3 style={styles.fileName}>
                {selectedFile.name}
              </h3>

              <p style={styles.successText}>
                Image selected successfully.
              </p>


              <div style={styles.buttonRow}>

                <button
                  type="button"
                  onClick={
                    handleChooseAnother
                  }
                  style={styles.primaryButton}
                >
                  Choose Another
                </button>


                <button
                  type="button"
                  onClick={handleRemove}
                  style={styles.removeButton}
                >
                  Remove
                </button>

              </div>


              <button
                type="button"
                onClick={handleAnalyze}
                disabled={loading}
                style={styles.analyzeButton}
              >
                {loading
                  ? "Analyzing..."
                  : "Analyze Medicine"}
              </button>


              {error && (
                <div style={styles.error}>
                  {error}
                </div>
              )}

            </div>
          )}


          {result && (

            <section style={styles.resultSection}>

              <h2 style={styles.resultTitle}>
                Analysis Result
              </h2>


              <div style={styles.resultGrid}>

                <div style={styles.resultCard}>
                  <p style={styles.resultLabel}>
                    Medicine
                  </p>

                  <p style={styles.resultValue}>
                    {result.medicine
                      ?.medicine_name ||
                      "Not available"}
                  </p>
                </div>


                <div style={styles.resultCard}>
                  <p style={styles.resultLabel}>
                    Strength
                  </p>

                  <p style={styles.resultValue}>
                    {result.medicine
                      ?.strength ||
                      "Not available"}
                  </p>
                </div>


                <div style={styles.resultCard}>
                  <p style={styles.resultLabel}>
                    Form
                  </p>

                  <p style={styles.resultValue}>
                    {result.medicine
                      ?.form ||
                      "Not available"}
                  </p>
                </div>


                <div style={styles.resultCard}>
                  <p style={styles.resultLabel}>
                    Category
                  </p>

                  <p style={styles.resultValue}>
                    {result.classification
                      ?.category ||
                      "Not available"}
                  </p>
                </div>


                <div style={styles.resultCard}>
                  <p style={styles.resultLabel}>
                    Instructions
                  </p>

                  <p style={styles.resultValue}>
                    {result.medicine
                      ?.instructions ||
                      "Not available"}
                  </p>
                </div>


                <div style={styles.resultCard}>
                  <p style={styles.resultLabel}>
                    Expiration Date
                  </p>

                  <p style={styles.resultValue}>
                    {result.medicine
                      ?.expiration_date ||
                      "Not available"}
                  </p>
                </div>

              </div>


              {result.explanation && (

                <div
                  style={
                    styles.explanationCard
                  }
                >

                  <h3
                    style={{
                      marginTop: 0,
                      color: isDark
                        ? "#ffffff"
                        : "#0b2545",
                    }}
                  >
                    Simplified Explanation
                  </h3>

                  <p style={styles.explanation}>
                    {result.explanation}
                  </p>

                </div>
              )}


              <div style={styles.disclaimer}>
                <strong>Disclaimer:</strong>{" "}
                MediLens provides simplified
                information from the uploaded
                medicine label. It is not a
                diagnosis or a prescription.
                Do not change your medication
                or dosage based only on this
                information. Consult a qualified
                healthcare professional when
                needed.
              </div>

            </section>
          )}

        </main>

      </Show>

    </div>
  );
}


export default App;