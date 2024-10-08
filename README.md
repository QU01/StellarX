# StellarX Project

StellarX is an interactive web application designed to engage users in conversations about exoplanets. It leverages advanced language models to generate and evaluate questions, manage conversations, and provide detailed information about exoplanets.

This project was created for NASA Space Apps

## Features

- **Conversation Management**: Stores, retrieves, and deletes chat conversations.
- **Question Generation**: Creates questions about exoplanets using language models.
- **Response Evaluation**: Scores user responses to exoplanet-related questions.
- **Exoplanet Management**: Allows creation and retrieval of exoplanet data.

## Technologies Used

- **Backend**: Django and Django REST Framework.
- **Frontend**: React.
- **Language Models**: Langchain and OpenAI.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/stellarx.git
   ```
2. Navigate to the project directory:
   ```bash
   cd stellarx
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install frontend dependencies:
   ```bash
   npm install
   ```

## Usage

### Backend

1. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

### Frontend

1. Start the React application:
   ```bash
   npm start
   ```

## API Endpoints

- **Chat**: `/api/chat/` - Retrieve chat history and create new conversations.
- **Generate Questions**: `/api/generar_preguntas_exoplaneta/` - Generate questions about an exoplanet.
- **Evaluate Responses**: `/api/calificar_respuestas_exoplaneta/` - Evaluate user responses.
- **Create Exoplanet**: `/api/crear_exoplaneta/` - Create new exoplanets.
- **Get Exoplanets**: `/api/obtener_exoplanetas/` - Retrieve exoplanet data.

## OpenAI API Key

To use the language model features, you need an OpenAI API key. Follow these steps to obtain one:

1. Visit the [OpenAI website](https://openai.com/).
2. Sign up for an account if you don't have one.
3. Navigate to the API section and generate a new API key.
4. Copy the API key and replace the placeholder in your code with this key.

## Contribution

If you wish to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push your changes to the branch (`git push origin feature/new-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
