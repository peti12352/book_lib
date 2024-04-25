function returnBook(bookId) {
    fetch(`/return-book/${bookId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          window.location.reload();
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  
  function rentBook(bookId) {
    fetch(`/rent-book/${bookId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          window.location.reload();
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }