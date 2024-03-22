_notify = new deciresAlert();

const retrieveProfessionalPublicQuery = `
query professionalRetrievePublicQuery($input: QueryRetrieveUserInput!) {
  psychology {
    getProfessional(input: $input) {
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
      facebookProfile
      instagramProfile
      linkedinProfile
      userCarreerSet {
        originalId
        name
        description
        serviceMethodEnum
        serviceModalityEnum
        experienceSummary
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

const contactMe = `mutation contactMe($input: MutationContactMeInput!) {
  psychology {
    contactMe(input: $input) {
      __typename
      ... on ContactMeType {
        originalId
        wasReported
        __typename
      }
      ... on ResponseValidationError {
        code
        type
        message
        __typename
      }
      ... on ResponseInternalError {
        code
        type
        message
        __typename
      }
      ... on ResponseIntegrityError {
        code
        type
        message
        __typename
      }
    }
  }
}`;

function htmlComponentDisplay($data) {
  this.data = $data;

  this.splitParagraph = (paragraph) => {
    let $paragraph = paragraph.split(/\. (?=[A-Z])/);

    var outParagraph = "";

    for (var i = 0; i < $paragraph.length; i++) {
      outParagraph += `<p class="about-me-desc" style="text-align: justify;">${$paragraph[i]}</p>`;
    }
    return outParagraph;
  };
  this.renderProfile = () => {
    obj = this.data;
    userCarreer = obj.userCarreerSet[0];
    expParagraph = this.splitParagraph(userCarreer.experienceSummary);

    emailIcon = `<span class="fa-stack fa-1x text-inverse">
        <i class="fa fa-envelope fa-stack-1x"></i>
      </span>`;
    linkedInIcon = `<span class="fa-stack fa-1x text-inverse">
        <i class="fab fa-linkedin fa-stack-1x"></i>
      </span>`;
    facebookIcon = `<span class="fa-stack fa-1x text-inverse">
        <i class="fab fa-facebook fa-stack-1x"></i>
      </span>`;
    instagramIcon = `<span class="fa-stack fa-1x text-inverse">
        <i class="fab fa-instagram fa-stack-1x"></i>
      </span>`;

    $avatar = obj.avatar ? obj.avatar.url : "";

    return `<div class="post-image" style="text-align: center;">
                <img style="max-width: 200px; height: auto;" src="${$avatar}" class="img-fluid">
            </div>
            </br>
            <h2 class="content-title">${obj.firstName} ${obj.lastName} (${userCarreer.name})</h2>
            <hr>
            <h3 class="content-title"><i class="fa fa-globe"></i> Redes Sociales</h3>
            <h4 class="content-title">
              <small>
                ${emailIcon}
                ${obj.email || ""}
              </small>
            </h4>
            <h4 class="content-title">
              <small>
                ${linkedInIcon}
                ${obj.linkedinProfile || ""}
              </small>
            </h4>
            <h4 class="content-title">
              <small>
                ${facebookIcon}
                ${obj.facebookProfile || ""}
              </small>
            </h4>
            <h4 class="content-title">
              <small>
                ${instagramIcon}
                ${obj.instagramProfile || ""}
              </small>
            </h4>
            <hr>
            <h4 class="content-title">Tipo de atención:
              <small>
                ${userCarreer.serviceMethodEnum}
              </small>
            </h4>
            <h4 class="content-title">Modalidad de atención:
              <small>
                ${userCarreer.serviceModalityEnum}
              </small>
            </h4>

            <br>
            <h3 class="content-title">Sobre Mi</h3>
            <br>
            <div class="parrafos">
                ${expParagraph}
            </div>
            <br>`;
  };
  this.renderSpecializations = () => {
    $data = this.data.userSpecializationSet;

    $specializations = "";
    for ($i = 0; $i < $data.length; $i++) {
      $specializations += `<li style="list-style: none;"><a href="javascript:void(0)" style="text-decoration: none; color: black;">${$data[$i].name}.</a></li>`;
    }
    return $specializations;
  };
  this.renderLanguages = () => {
    $data = this.data.languagesSet;

    $languages = "";
    for ($i = 0; $i < $data.length; $i++) {
      $languages += `<li style="list-style: none;"><a href="javascript:void(0)" style="text-decoration: none; color: black;">${$data[$i].name}.</a></li>`;
    }
    return $languages;
  };
  this.renderOfficeLocations = () => {
    $data = this.data.userOfficeSet;

    $locations = "";
    for ($i = 0; $i < $data.length; $i++) {
      $locations += `<li style="list-style: none;"><a href="javascript:void(0)" style="text-decoration: none; color: black;">${$data[$i].name}, ${$data[$i].city.name}.</a></li>`;
    }
    return $locations;
  };
}

initialRequest = () => {
  $.ajax({
    url: Django.graphql_url,
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      query: retrieveProfessionalPublicQuery,
      variables: {
        input: {
          originalId: originalId,
        },
      },
    }),
    success: function (response) {
      $data = [];

      if (response.data && response.data.psychology && response.data.psychology.getProfessional) {
        $data = response.data.psychology.getProfessional;

        html = new htmlComponentDisplay($data);
        $profile = html.renderProfile();
        $languages = html.renderLanguages();
        $specializations = html.renderSpecializations();
        $office_locations = html.renderOfficeLocations();

        $("#profile").empty().append($profile);
        $("#languages").empty().append($languages);
        $("#specializations").empty().append($specializations);
        $("#office_locations").empty().append($office_locations);
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

loadModal = () => {
  // $("#masked-input-phone").mask("+54 (999) 999.99.99");

  $("#modal_send_message").modal("show");
  return false;
};

sendMessage = () => {
  $.ajax({
    url: Django.graphql_url,
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      query: contactMe,
      variables: {
        input: {
          userId: originalId.toString(),
          fullName: $("#full_name").val(),
          email: $("#email").val(),
          phone: $("#phone").val(),
          message: $("#message").val(),
        },
      },
    }),
    success: function (response) {
      $data = response.data.psychology.contactMe;
      notification = new deciresAlert();
      if (
        response.data &&
        response.data.psychology &&
        response.data.psychology.contactMe &&
        response.data.psychology.contactMe.originalId
      ) {
        $.when($("#modal_send_message").modal("hide")).then(
          notification.basic("Éxito", "Su mensaje ha sido enviado", "success")
        );
      } else {
        $.when($("#modal_send_message").modal("hide")).then(
          notification.basic("Lo sentimos, algo salió mal", $data.message, "error")
        );
      }
      return false;
    },
    error: function (xhr, status, error) {
      console.error("Error en la solicitud AJAX:", status, error);
      notification = new deciresAlert();
      $.when($("#modal_send_message").modal("hide")).then(
        notification.basic("Ups!", "Lo sentimos, algo salió mal", "error")
      );
      setTimeout(function () {
        location.href = Django.urls.home;
      }, 40);
    },
  });
  return false;
};
