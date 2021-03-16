import { render, screen, fireEvent } from '@testing-library/react';
import App from './App';

test('showLogin disappears', () => {
  const result = render(<App />);

  const loginButtonElement = screen.getByText('Login');
  expect(loginButtonElement).toBeInTheDocument();

  fireEvent.click(loginButtonElement);
});
// test("Login Flow", () => {
//   render(<App />);
//   const linkElement = screen.getByText(/learn react/i);
//   expect(linkElement).toBeInTheDocument();
// });

// test("Board Clicking", () => {
//   render(<App />);
//   const linkElement = screen.getByText(/learn react/i);
//   expect(linkElement).toBeInTheDocument();
// });
