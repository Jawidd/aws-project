import './CrudButton.css';

export default function CrudButton(props) {
  const pop_activities_form = (event) => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    props.setPopped(true);
  }

  return (
    <button onClick={pop_activities_form} className='post'>Crud</button>
  );
}
