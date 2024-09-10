# PilarEaseDJO

![PilarEase](main/static/images/homepage.png)
PilarEaseDJO is a Django-based platform for emotion management and sentiment analysis, featuring user authentication, status posting, emotion filtering, machine learning integration, chatbot interaction, and administrative tools.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/KCprsnlcc/PilarEaseDJO.git
   ```

2. Navigate to the project directory:

   ```sh
   cd PilarEaseDJO
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run migrations:

   ```sh
   python manage.py migrate
   ```

5. Start the development server:

   ```sh
   python manage.py runserver
   ```

6. Access the application at `http://localhost:8000`.

Here’s the updated **Features** section to include the referral module and the counselor chat interface:

---

## Features

### 1. User Authentication & Management

- **Logins**: Allows users to log in using their credentials. Includes session management to maintain user login state.
- **Register**: Enables new users to create an account with validated input data saved to the database.
- **Forgot Password**: Provides a mechanism for users to reset their password via email.
- **Masterlist Verification**: Verifies user credentials against master list data during registration or login.

### 2. User Profile Management

- **User Profile Interface**: Allows users to view and update their profile information.
- **Password Management**: Enables users to manage and update their passwords securely.
- **Upload Avatar**: Allows users to upload and update their profile pictures.

### 3. Main Interface

- **Dashboard**: Provides a main interface for user interactions, including posting and viewing statuses.
- **About Interface**: Includes an informational page providing details about the portal.

### 4. Status Management

- **Status Posting**: Allows users to post updates. Includes a content filter to detect and block inappropriate content.
- **View Status**: Enables users to view statuses posted by themselves and others.
- **Reply to Status**: Allows users to reply to statuses, with replies saved to the database.
- **Referral Module**: Allows users to refer and report inappropriate statuses directly to a counselor for review. The counselor can block inappropriate content or take further action as needed.

### 5. Emotion Management

- **Emotion Filter Category**: Provides options to filter statuses based on different emotions for targeted viewing.

### 6. Data Collection

- **Emotion Dataset Collection**: Collects data on expressed emotions in English.

### 7. Machine Learning Integration

- **Pre-trained Model Collection**: Integrates suitable pre-trained models for emotion analysis.
- **Fine-Tuning Pre-trained Model**: Fine-tunes emotion analysis models using Tagalog datasets.
- **Analysis Model Deployment**: Deploys the fine-tuned sentiment analysis model within the portal.

### 8. Chatbot Integration

- **Chatbot Interface**: Provides an interface for chatbot interaction using an expert system with backward chaining, allowing smooth transitions between bot and live counselor interactions.
- **Chatbot Model Deployment**: Ensures real-time interaction and the seamless operation of the chatbot.

### 9. Contact & Support

- **Contact Interface**: Allows users to send messages via a contact form routed to administrators.
- **Message Queries**: Implements a system for users to send and receive responses to their queries.

### 10. Administrative Tools

- **View Text Message Queries**: Enables administrators to view user queries.

- **Emotion Category Search Filtering**: Allows filtering of searches by emotion categories.
- **Analysis Search Filtering**: Provides options to filter sentiment analysis results.
- **View Text Analysis Results**: Displays detailed sentiment analysis results for review.
- **Counselor Chat Interface**: Collects all questions and answers from chatbot interactions and allows counselors to chat in real-time with users. This interface enables counselors to manage and respond to reported statuses and provide personalized support.
- **Manage Users**: Includes tools for managing user profiles, including deactivation, deletion, and editing.
- **Download Analysis Data**: Allows exporting of sentiment analysis data in CSV format.

## Contributing

Contributions are welcome! Please follow the [Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [License](LICENSE.md).

## Support

For any inquiries or issues, please contact [kcpersonalacc@gmail.com](mailto:kcpersonalacc@gmail.com).

---

**Note:** This project is still in development. Some features may not be fully implemented or may change as the project evolves.
