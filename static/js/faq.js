
console.log('sdhfhdhhfhhdhfdhfdf');

document.addEventListener("DOMContentLoaded", () => {
  const wordItems = document.querySelectorAll('.word-item');

  const faqContent = {
    'faq-1': [
      { question: ' What is Buysel.in?', answer: ' Buysel.in connects buyers and sellers directly for property and scrap deals, ensuring a zero-commission, hassle-free experience.' },
      { question: 'How does Buysel.in work?', answer: 'Buysel.in enables users to list properties or scrap, connect with verified buyers or sellers, and enjoy a transparent, cost-effective experience.' },
      { question: 'What services does Buysel.in offer?', answer: 'Buysel.in connects buyers and sellers directly on a commission-free platform, ensuring secure, verified listings. It offers a transparent and hassle-free experience across real estate and e-waste transactions.' },
      { question: 'Is Buysel.in free to use?', answer: 'Users can explore listings for free, while a small fee applies for posting properties or scrap materials for sale, rent or lease, ensuring a high-quality, reliable marketplace for all.' },

    ],
    'faq-2': [
      { question: ' Are the property listings on Buysel.in verified?', answer: 'Yes, all property and scrap listings on Buysel.in are verified to ensure security and prevent fraud, giving buyers peace of mind.' },
      { question: 'Can I directly contact property owners on Buysel.in?', answer: 'Yes, Buysel.in facilitates direct communication between buyers and sellers, eliminating the need for brokers or middlemen.' },
      { question: 'Does Buysel.in provide detailed property information?', answer: 'Yes, each property listing includes detailed descriptions, images, location on a map, and the seller’s contact information for clarity and convenience.' },
      { question: 'Can I negotiate prices with sellers on Buysel.in?', answer: 'Yes, buyers and sellers can directly negotiate the terms of the transaction through the contact information provided in the listings.' },



    ],
    'faq-3': [
      { question: 'How do I list my property or scrap material on Buysel.in?', answer: 'To list property or scrap material on Buysel.in, simply click on the "Add Property" or "Add Listing" option available on the website, fill in the required details, and upload relevant images or descriptions to complete listing.' },
      { question: 'What property categories can I post on Buysel.in?', answer: 'Buysel.in allows sellers to list residential, commercial, and land properties, connecting them directly with buyers for a transparent, profitable experience.' },
      { question: 'Is there a limit to how many listings I can post?', answer: ' Individual users can post listings as needed, while brokers have access to an admin panel allowing unlimited listings for one year.' },
      { question: 'How do I ensure my property gets more visibility?', answer: ' To improve visibility, provide accurate details, upload high-quality images, and choose relevant categories while listing your property or scrap material.' },
      { question: 'What types of scrap materials can I list on Buysel.in?', answer: 'Buysel.in connects sellers with buyers for e-waste, metal scraps, and various recyclable materials.' },

    ],
    'faq-4': [
      { question: 'How does Buysel.in ensure the authenticity of users?', answer: 'Buysel.in verifies all users through their login credentials and location verification process to maintain a secure platform for transactions.' },
      { question: 'What measures does Buysel.in take to prevent fraud?', answer: 'Buysel.in offers verified listings, direct buyer-seller communication, and dedicated support for dispute resolution.' },

    ],
    'faq-5': [
      { question: 'What are the advantages of using Buysel.in for property transactions?', answer: 'Buysel.in removes brokerage fees, enabling secure, transparent, and direct transactions between verified buyers and sellers.' },
      { question: 'How does Buysel.in help in scrap and e-waste management?', answer: 'The platform provides an easy way to buy or sell scrap materials, promoting responsible recycling and waste management practices.' },
      { question: 'Why should I choose Buysel.in over traditional brokers?', answer: 'Buysel.in saves you money by eliminating brokerage fees and ensures a hassle-free experience with verified listings and a user-friendly interface.' },


    ],

    'faq-6': [
      { question: 'What should I do if I face issues while using Buysel.in?', answer: 'Users can contact Buysel.in dedicated customer support team for assistance and query resolution.' },
      { question: 'How do I contact Buysel.in for support?', answer: 'Visit the “Contact Us” section on the website or app for customer care details. Alternatively, you can submit your queries directly through the platform.' },
      { question: 'Is there any enquiry  to guide users on how to post a listing?', answer: 'Our website features a dedicated contact page with an enquiry form. Please fill out the form with your details and submit it for prompt assistance.' },


    ],

  };
  function updateFAQContent(faqId) {
    console.log(faqId, 'this is itemmm..');
    const faqContainer = document.getElementById('faq-content');
    const rotatingArrow = document.getElementById('rotating-arrow');
    console.log(faqContainer, 'containereererer');

    faqContainer.innerHTML = ''; // Clear previous content

    const faqItems = faqContent[faqId]; // Get the items for the selected FAQ

    faqItems.forEach((item,i) => {


      const faqItem = document.createElement('div');
      faqItem.classList.add('faq-item');

      const question = document.createElement('div');
      question.classList.add('faq-question');
      question.innerHTML = `
            <span>${item.question}</span>
            <img src="/static/img/Vector.svg" alt="Expand" id='${i}' class="toggle-icon" />
          `;

      const answer = document.createElement('div');
      answer.classList.add('faq-answer-content');
      answer.style.display = 'none';
      answer.innerHTML = `<p>${item.answer}</p>`;

      faqItem.appendChild(question);
      faqItem.appendChild(answer);
      faqContainer.appendChild(faqItem);
      faqContainer.appendChild(document.createElement('hr'));
    });

    // Toggle FAQ answers when clicked
    document.querySelectorAll(".faq-item").forEach((item) => {
      const question = item.querySelector(".faq-question");
      const answer = item.querySelector(".faq-answer-content");
      const icon = question.querySelector(".toggle-icon");

      question.addEventListener("click", () => {
        console.log('gdfdf');
        
        const isExpanded = answer.style.display === "block";



        document.querySelectorAll(".faq-answer-content").forEach((ans) => {
          ans.style.display = "none";
        });

        let rotatingStatus = false

        document.querySelectorAll(".toggle-icon").forEach((ic) => {
          icon.src = "/static/img/Vector.svg";
          console.log(icon.id,'this is the expanded id');

          console.log(icon.style.transform,'confirmmm');
          
          if(isExpanded){
            console.log();
            
            icon.style.transform = `rotate(0deg)`;
            rotatingStatus = true
            
          }else{
            icon.style.transform = `rotate(180deg)`;
            rotatingStatus = false

          }
            


          
        });

        if (!isExpanded) {
          answer.style.display = "block";
          // icon.src = "/static/img/Vector.svg";
          // console.log(icon.id,'this is not expanded');


        }
      });

      answer.addEventListener("click", () => {
        console.log(icon,'icccioonnn');
        
        answer.style.display = "none";
        icon.src = "/static/img/Vector.svg";
        icon.style.transform = `rotate(0deg)`;

      });
    });
  }

  // Add event listeners for both mobile and desktop word-items
  wordItems.forEach(word => {
    word.addEventListener('click', () => {
      const faqId = word.getAttribute('data-faq');
      updateFAQContent(faqId);
    });
  });

  // Initialize with the first FAQ
  updateFAQContent('faq-1');

  // Highlight the selected button
  document.querySelectorAll('.word-item').forEach(item => {
    item.addEventListener('click', function () {
      document.querySelectorAll('.word-item h1').forEach(el => {
        el.classList.remove('text-[#8bc83f]');
      });

      this.querySelector('h1').classList.add('text-[#black]');
    });
  });
});












document.addEventListener('DOMContentLoaded', () => {
  // Select all buttons
  const buttons = document.querySelectorAll('.faq-button');

  // Function to remove the active class from all buttons
  function removeActiveClass() {
    buttons.forEach(button => {
      button.classList.remove('bg-[#8bc83f]', 'text-white');
    });
  }

  // Add event listener to each button to toggle the active class
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      // First, remove active classes from all buttons
      removeActiveClass();

      // Now, add the active class to the clicked button
      button.classList.add('bg-[#8bc83f]', 'text-black');

      console.log("Button clicked:", button);  // For debugging

    });
  });
});













document.addEventListener("DOMContentLoaded", () => {
  const wordItems = document.querySelectorAll('.word-item');

  // Set initial color of 'General questions' to #8bc83f, but only for larger screens
  if (window.innerWidth > 768) {
    document.querySelector('#general').classList.add('active');
  }

  // Add event listeners to all word items
  wordItems.forEach(word => {
    word.addEventListener('click', () => {
      // Reset all h1 elements' colors to black
      document.querySelectorAll('.word-item h1').forEach(h1 => {
        h1.classList.remove('active');
        h1.style.color = 'black';  // Reset color to default
      });

      // Set clicked h1 to #8bc83f only if the screen size is larger than mobile
      if (window.innerWidth > 768) {
        const clickedH1 = word.querySelector('h1');
        clickedH1.classList.add('active');
        clickedH1.style.color = '#8bc83f'; // Apply the active color
      }
    });
  });
});
