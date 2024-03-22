# Third-party Libraries
import strawberry

# Own Libraries
from apps.psychology.schema.mutations import ProfessionalMutations
from apps.psychology.schema.queries import ProfessionalQueries, Select2Queries


@strawberry.type
class QueriesSummary(
    ProfessionalQueries,
):
    pass


@strawberry.type()
class MutationSummary(
    ProfessionalMutations,
):
    pass


@strawberry.type()
class Queries:
    @strawberry.field()
    async def select2(self) -> Select2Queries:
        return Select2Queries()

    @strawberry.field()
    async def psychology(self) -> QueriesSummary:
        return QueriesSummary()


@strawberry.type()
class Mutations:
    @strawberry.field()
    async def psychology(self) -> MutationSummary:
        return MutationSummary()


schema = strawberry.Schema(query=Queries, mutation=Mutations)
