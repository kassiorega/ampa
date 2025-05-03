from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.models.models import db, Animal, Adotante
from sqlalchemy.exc import IntegrityError

animal_bp = Blueprint(\'animal\', __name__, url_prefix=\'/animal\')

@animal_bp.route(\'/cadastrar\', methods=[\'GET\', \'POST\'])
def cadastrar_animal():
    if request.method == \'POST\':
        # Dados do Tutor
        nome_tutor = request.form.get(\'nome_tutor\')
        cpf_tutor = request.form.get(\'cpf\')
        email_tutor = request.form.get(\'email\')
        telefone_tutor = request.form.get(\'telefone\')
        endereco_tutor = request.form.get(\'endereco\')

        # Dados do Animal
        numero_chip = request.form.get(\'numero_chip\')
        nome_animal = request.form.get(\'nome_animal\')
        especie = request.form.get(\'especie\')
        raca = request.form.get(\'raca\')
        idade = request.form.get(\'idade\')
        sexo = request.form.get(\'sexo\')
        porte = request.form.get(\'porte\')
        saude = request.form.get(\'saude\')
        historico = request.form.get(\'historico\')

        # Validações básicas
        if not all([nome_tutor, cpf_tutor, email_tutor, telefone_tutor, endereco_tutor, numero_chip, especie]):
            flash(\'Erro: Todos os campos obrigatórios do tutor e do animal (chip, espécie) devem ser preenchidos.\', \'error\')
            return render_template(\'cadastro_animal.html\')

        try:
            # Verificar/Criar Tutor
            tutor = Adotante.query.filter((Adotante.cpf == cpf_tutor) | (Adotante.email == email_tutor)).first()
            if not tutor:
                tutor = Adotante(
                    nome=nome_tutor,
                    cpf=cpf_tutor,
                    email=email_tutor,
                    telefone=telefone_tutor,
                    endereco=endereco_tutor
                )
                db.session.add(tutor)
                # Commit tutor first to get ID if needed, or rely on SQLAlchemy relationship management
                db.session.flush() # Get the ID before associating

            # Verificar se animal com este chip já existe
            animal_existente = Animal.query.filter_by(numero_chip=numero_chip).first()
            if animal_existente:
                flash(f\'Erro: Já existe um animal cadastrado com o chip {numero_chip}.\', \'error\')
                return render_template(\'cadastro_animal.html\')

            # Criar Animal
            novo_animal = Animal(
                numero_chip=numero_chip,
                nome=nome_animal,
                especie=especie,
                raca=raca,
                idade=int(idade) if idade and idade.isdigit() else None,
                sexo=sexo,
                porte=porte,
                saude=saude,
                historico=historico,
                status=\'registrado com tutor\', # Status específico
                id_adotante=tutor.id_adotante # Associa ao tutor
            )
            db.session.add(novo_animal)
            db.session.commit()
            flash(f\'Animal {nome_animal or "sem nome"} (Chip: {numero_chip}) cadastrado com sucesso para o tutor {nome_tutor}!\', \'success\')
            return redirect(url_for(\'animal.cadastrar_animal\'))

        except IntegrityError as e:
            db.session.rollback()
            error_info = str(e.orig).lower() # Get original DB error
            if \'adotantes_cpf_key\' in error_info or \'adotantes.cpf\' in error_info:
                 flash(f\'Erro: Já existe um tutor cadastrado com este CPF ({cpf_tutor}).\', \'error\')
            elif \'adotantes_email_key\' in error_info or \'adotantes.email\' in error_info:
                 flash(f\'Erro: Já existe um tutor cadastrado com este Email ({email_tutor}).\', \'error\')
            elif \'animais_numero_chip_key\' in error_info or \'animais.numero_chip\' in error_info:
                 flash(f\'Erro: Já existe um animal cadastrado com o chip {numero_chip}.\', \'error\')
            else:
                flash(f\'Erro de integridade ao salvar no banco: {e}\', \'error\')
        except Exception as e:
            db.session.rollback()
            flash(f\'Ocorreu um erro inesperado: {e}\', \'error\')

    return render_template(\'cadastro_animal.html\')

# Rota para a página principal (consulta)
@animal_bp.route(\'/consultar\', methods=[\'GET\', \'POST\'])
def consultar_animal():
    animal = None
    numero_chip_pesquisado = \'\'
    if request.method == \'POST\':
        numero_chip = request.form.get(\'numero_chip\')
        numero_chip_pesquisado = numero_chip # Keep search term in input
        if numero_chip:
            # Usar options(joinedload(Animal.tutor)) para carregar o tutor junto (evita query N+1)
            # from sqlalchemy.orm import joinedload
            # animal = Animal.query.options(joinedload(Animal.tutor)).filter_by(numero_chip=numero_chip).first()
            animal = Animal.query.filter_by(numero_chip=numero_chip).first()
            if not animal:
                flash(f\'Nenhum animal encontrado com o chip {numero_chip}.\', \'info\')
        else:
            flash(\'Por favor, digite um número de chip para consultar.\', \'error\')

    return render_template(\'consulta_animal.html\', animal=animal, numero_chip_pesquisado=numero_chip_pesquisado)

