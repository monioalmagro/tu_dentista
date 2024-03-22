$request_values = DecireslocalStorage.get("request_values");

const filter_type_especializations = 1;
const filter_type_language = 2;
/**
 * GraphQL query to retrieve the list of public professionals.
 */
const listProfessionalPublicQuery = `
query professionalListPublicQuery($input: QueryListUserInput!) {
  psychology {
    getProfessionalList(input: $input) {
      originalId
      firstName
      lastName
      email
      avatar {
        originalId
        url
        __typename
      }
      genderEnum
      attentionSchedule
      facebookProfile
      instagramProfile
      linkedinProfile
      userCarreerSet {
        originalId
        name
        description
        serviceMethodEnum
        serviceModalityEnum
        truncateExperienceSummary
        __typename
      }
      userSpecializationSet {
        originalId
        name
        description
        __typename
      }
      languagesSet {
        name
        slug
        flagIcon
        __typename
      }
      userOfficeSet {
        name
        city {
          name
          __typename
        }
        __typename
      }
      attachmentSet {
        originalId
        url
        description
      }
      isVerifiedProfile
      profileUrl
      __typename
    }
  }
}
`;

/**
 * Generates HTML for an item row.
 */
getItemRow = (items) => {
  return `<div class="item-row">${items}</div>`;
};
/**
 * Generates HTML for an item.
 */
getItem = (obj) => {
  const specializations = obj.userSpecializationSet.flatMap((item) => item.name).join(", ");

  let specialization_word =
    obj.userSpecializationSet.length > 1 ? "Especialidades:" : "Especialidad:";

  let $avatar = obj.avatar ? obj.avatar.url : "";

  return `<div class="item item-thumbnail">
            <a href="${obj.profileUrl}" class="item-image">
              <img src="${$avatar}" alt="${obj.firstName} ${obj.lastName}" />
            </a>
            <div class="item-info">
              <h4 class="item-title">
                <a href="${obj.profileUrl}">${obj.firstName} ${obj.lastName} (${obj.userCarreerSet[0].name})</a>
              </h4>
              <p class="item-desc">${specialization_word}</p>
              <div class="item-price">${specializations}</div>

            </div>
          </div>`;
};

professional_filter_results = () => {
  const checkboxesSpecializationSelected = $('input[name="specializations"]:checked');
  const checkboxesLanguagesSelected = $('input[name="languages"]:checked');
  const $filterSet = new Set();

  checkboxesSpecializationSelected.each(function () {
    const label = $('label[for="' + this.id + '"]');
    $filterSet.add(label.text());
  });
  checkboxesLanguagesSelected.each(function () {
    const label = $('label[for="' + this.id + '"]');
    $filterSet.add(label.text());
  });

  if ($filterSet.size > 0) {
    let filtros = Array.from($filterSet);

    professionalSearchController.filter_list = filtros.map((cadena) => cadena.trim());
    professionalSearchController.getFilteredResults();
    professionalSearchController.updatePagination();
    professionalSearchController.filter_list = [];
  }

  return false;
};

/**
 * Restores filters to the initial state.
 */
restore_filters = () => {
  const checkboxesSpecializationSelected = $('input[name="specializations"]:checked');
  const checkboxesLanguagesSelected = $('input[name="languages"]:checked');
  checkboxesSpecializationSelected.prop("checked", false);
  checkboxesLanguagesSelected.prop("checked", false);
  //
  professionalSearchController.filter_list = [];
  professionalSearchController.getInitialSearchResults();
  return false;
};

function htmlFilterSection(data) {
  this.data = data;

  this.process_html_id = (itemName, itemPropertyName) => {
    // Convierte a minúsculas y reemplaza espacios por guiones bajos
    const processName = `${itemName.toLowerCase()}_${itemPropertyName
      .toLowerCase()
      .replace(/\s/g, "_")}`;
    return processName;
  };

  this.setCheckBockItem = (itemName, item, itemPropertyName, checkboxName) => {
    $input_id = this.process_html_id(itemName, item.name || item.languageName);
    return `
    <div class="form-check">
      <input type="checkbox" class="form-check-input" id=${$input_id} name=${checkboxName} />
      <label class="form-check-label" for=${$input_id}>${item[itemPropertyName]}<label>
    </div>`;
  };

  this.setupFilter = (itemName, itemPropertyName, html_id, checkboxName) => {
    $htmlItemList = "";
    $items = this.data;

    for (const $item of $items) {
      $htmlItemList += this.setCheckBockItem(itemName, $item, itemPropertyName, checkboxName);
    }

    $(html_id).empty().append($htmlItemList);

    return false;
  };
}

/**
 * Controller class for managing professional search functionality.
 */
let professionalSearchController = {
  data: null,
  total_count: null,
  filtered_total_count: null,
  filter_list: [],
  currentPage: 1,
  itemsPerPage: 12,

  /**
   * Initializes the controller with data.
   */
  init: function ($data) {
    this.data = $data;
  },
  /**
   * Gets the total count of items and updates the UI.
   */
  getTotalCount: function () {
    this.total_count = this.data.length;
    this.filtered_total_count = this.data.length;
    $("#total_count").text(this.filtered_total_count + " de " + this.total_count);
    return false;
  },
  /**
   * Generates sidebar items for specializations and updates the UI.
   */
  getSideBarSpecializations: function (key, html_id) {
    $data = [];
    this.data.forEach((items) => {
      const $specializations = items.userSpecializationSet;
      $specializations.forEach((items2) => {
        const isObjectNotPresent = !$data.some((dataItem) => {
          return dataItem.name === items2.name;
        });
        if (isObjectNotPresent) {
          $data.push(items2);
        }
      });
    });

    filter = new htmlFilterSection($data);
    filter.setupFilter("specialization", "name", html_id, "specializations");
    return false;
  },
  /**
   * Generates sidebar items for languages and updates the UI.
   */
  getSideBarLanguages: function (html_id) {
    $data = [];

    this.data.forEach((items) => {
      const $languages = items.languagesSet;

      $languages.forEach((items2) => {
        const isObjectNotPresent = !$data.some((dataItem) => {
          return dataItem.name === items2.name;
        });

        if (isObjectNotPresent) {
          $data.push(items2);
        }
      });
    });

    filter2 = new htmlFilterSection($data);
    filter2.setupFilter("language", "name", html_id, "languages");
    return false;
  },
  /**
   * Filters results based on the selected item and type.
   */
  getFilteredResults: function () {
    $data = this.filterData(this.data, this.filter_list);
    this.filtered_total_count = $data.length;
    $("#total_count").text(this.filtered_total_count + " de " + this.total_count);
    this.prepareResults($data);
    return false;
  },
  /**
   * Retrieves the initial search results.
   */
  getInitialSearchResults: function () {
    this.getTotalCount();
    $data = this.filterData(this.data, this.filter_list);
    this.prepareResults($data);
    return false;
  },
  /**
   * Prepare results.
   */
  prepareResults: function ($data) {
    $item_rows = ``;
    $html_items = [];

    for ($i = 0; $i < $data.length; $i++) {
      $html_items.push(getItem($data[$i]));
    }
    for ($j = 0; $j < $html_items.length; $j += 3) {
      $item_rows += getItemRow($html_items.slice($j, $j + 3));
    }
    $("#professional_list").empty().append($item_rows);
    return false;
  },

  filterData: function ($data, filterList) {
    if (filterList.length === 0) {
      return $data;
    }
    return $data.filter((professional) => {
      return filterList.some((filter) => {
        const specializationMatch = professional.userSpecializationSet.some(
          (s) => s.name === filter
        );
        const languageMatch = professional.languagesSet.some((l) => l.name === filter);
        return specializationMatch || languageMatch;
      });
    });
  },
  /**
   * Actualiza la paginación.
   */
  updatePagination: function () {
    const totalPages = Math.ceil(this.filtered_total_count / this.itemsPerPage);
    const paginationElement = $("#pagination");
    paginationElement.empty();

    // Crea el botón "Previo"
    paginationElement.append(
      `<li class="page-item ${
        this.currentPage === 1 ? "disabled" : ""
      }"><a href="javascript:;" class="page-link" onclick="professionalSearchController.changePage(${
        this.currentPage - 1
      })">Previo</a></li>`
    );

    // Crea los botones para cada página
    for (let i = 1; i <= totalPages; i++) {
      paginationElement.append(
        `<li class="page-item ${
          this.currentPage === i ? "active" : ""
        }"><a class="page-link" href="javascript:;" onclick="professionalSearchController.changePage(${i})">${i}</a></li>`
      );
    }

    // Crea el botón "Siguiente"
    paginationElement.append(
      `<li class="page-item ${
        this.currentPage === totalPages ? "disabled" : ""
      }"><a href="javascript:;" class="page-link" onclick="professionalSearchController.changePage(${
        this.currentPage + 1
      })">Siguiente</a></li>`
    );
  },

  /**
   * Cambia a la página especificada y actualiza la paginación.
   */
  changePage: function (page) {
    this.currentPage = page;
    this.prepareResults(this.data.slice((page - 1) * this.itemsPerPage, page * this.itemsPerPage));
    this.updatePagination();
  },
};

initialRequest = () => {
  $.ajax({
    url: Django.graphql_url,
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      query: listProfessionalPublicQuery,
      variables: $request_values,
    }),
    success: function (response) {
      $data = [];

      if (
        response.data &&
        response.data.psychology &&
        response.data.psychology.getProfessionalList
      ) {
        $data = response.data.psychology.getProfessionalList;

        Promise.resolve(
          professionalSearchController.init($data),
          professionalSearchController.getSideBarSpecializations(
            "userSpecializationSet",
            "#specialization_list"
          ),
          professionalSearchController.getSideBarLanguages("#language_list")
        ).then(function () {
          professionalSearchController.getInitialSearchResults();
          professionalSearchController.updatePagination();
        });
      } else {
        setTimeout(function () {
          location.href = Django.urls.home;
        }, 40);
      }
    },
    error: function (xhr, status, error) {
      console.error("Error en la solicitud AJAX:", status, error);
      setTimeout(function () {
        location.href = Django.urls.home;
      }, 40);
    },
  });
};

initialRequest();
